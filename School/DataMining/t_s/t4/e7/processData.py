"""Ejercicio 7 - MLP Pima Indians Diabetes. Ejecutar junto a diabetes(1).csv.
Dependencias: pip install numpy pandas matplotlib scikit-learn torch
"""
from pathlib import Path
import copy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch  # type: ignore[reportMissingImports]
from torch import nn  # type: ignore[reportMissingImports]
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, ConfusionMatrixDisplay)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'diabetes.csv'
OUT = ROOT / 'resultados_ejercicio7'
OUT.mkdir(exist_ok=True)
SHOW_PLOTS = True  # Cambia a False si solo deseas guardar las gráficas.
SEED = 42
EPOCHS = 60
BATCH_SIZE = 32
LR = 0.001
DEVICE = 'cpu'
torch.set_num_threads(2)
INVALID_ZERO = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
ARCHITECTURES = {'[8]': (8,), '[16,8]': (16, 8), '[32,16,8]': (32, 16, 8)}


def seed_everything(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=170, bbox_inches='tight')
    if SHOW_PLOTS:
        plt.show()
    plt.close()


def preprocessing():
    return Pipeline([('imputer', SimpleImputer(strategy='median')),
                     ('scaler', StandardScaler())])


class MLP(nn.Module):
    def __init__(self, hidden, dropout=0.0):
        super().__init__()
        layers = []
        previous = 8
        for units in hidden:
            layers += [nn.Linear(previous, units), nn.ReLU()]
            if dropout:
                layers.append(nn.Dropout(dropout))
            previous = units
        layers.append(nn.Linear(previous, 1))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        # BCEWithLogitsLoss incorpora sigmoide numéricamente estable.
        return self.network(x).squeeze(-1)


def evaluate(model, x, y):
    model.eval()
    with torch.no_grad():
        logits = model(torch.as_tensor(x, dtype=torch.float32))
        loss = nn.functional.binary_cross_entropy_with_logits(
            logits, torch.as_tensor(y, dtype=torch.float32)).item()
        probability = torch.sigmoid(logits).numpy()
    predicted = (probability >= 0.5).astype(int)
    return loss, accuracy_score(y, predicted), probability


def train_network(x_train, y_train, x_val, y_val, hidden, strategy='Ninguna',
                  epochs=EPOCHS, seed=SEED):
    seed_everything(seed)
    model = MLP(hidden, dropout=0.2 if strategy == 'Dropout 0.2' else 0)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR,
                                 weight_decay=0.001 if strategy == 'L2' else 0)
    criterion = nn.BCEWithLogitsLoss()
    x_tensor = torch.as_tensor(x_train, dtype=torch.float32)
    y_tensor = torch.as_tensor(y_train, dtype=torch.float32)
    history = []
    best_state, best_loss, wait = None, float('inf'), 0
    for epoch in range(epochs):
        model.train()
        generator = torch.Generator().manual_seed(seed + epoch)
        for batch in torch.randperm(len(y_tensor), generator=generator).split(BATCH_SIZE):
            optimizer.zero_grad()
            loss = criterion(model(x_tensor[batch]), y_tensor[batch])
            if strategy == 'L1':
                loss = loss + 0.0001 * sum(p.abs().sum() for p in model.parameters())
            loss.backward()
            optimizer.step()
        tr_loss, tr_acc, _ = evaluate(model, x_train, y_train)
        val_loss, val_acc, _ = evaluate(model, x_val, y_val)
        history.append({'epoca': epoch + 1, 'loss_train': tr_loss,
                        'loss_validacion': val_loss, 'accuracy_train': tr_acc,
                        'accuracy_validacion': val_acc})
        if strategy == 'Early stopping':
            if val_loss < best_loss - 0.0005:
                best_loss = val_loss
                best_state = copy.deepcopy(model.state_dict())
                wait = 0
            else:
                wait += 1
                if wait >= 12:
                    break
    if strategy == 'Early stopping' and best_state is not None:
        model.load_state_dict(best_state)
    return model, pd.DataFrame(history)


def scores(y, probability):
    pred = (probability >= 0.5).astype(int)
    return {'accuracy': accuracy_score(y, pred),
            'precision': precision_score(y, pred, zero_division=0),
            'recall': recall_score(y, pred, zero_division=0),
            'F1': f1_score(y, pred, zero_division=0),
            'ROC_AUC': roc_auc_score(y, probability)}


def cv_experiment(x, y, hidden, strategy, label):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    rows = []
    for fold, (idx_train, idx_val) in enumerate(cv.split(x, y), 1):
        prep = preprocessing()
        xt = prep.fit_transform(x.iloc[idx_train])
        xv = prep.transform(x.iloc[idx_val])
        yt, yv = y.iloc[idx_train].to_numpy(), y.iloc[idx_val].to_numpy()
        model, _ = train_network(xt, yt, xv, yv, hidden, strategy, seed=SEED + fold)
        _, _, probability = evaluate(model, xv, yv)
        rows.append({'configuracion': label, 'fold': fold, **scores(yv, probability)})
        print(f'  {label}: fold {fold}/5 listo', flush=True)
    return pd.DataFrame(rows)


def plot_curves(history, filename, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, metric, ylabel in zip(axes, ['loss', 'accuracy'], ['Loss', 'Accuracy']):
        ax.plot(history['epoca'], history[f'{metric}_train'], label='Training')
        ax.plot(history['epoca'], history[f'{metric}_validacion'], label='Validación')
        ax.set_xlabel('Época')
        ax.set_ylabel(ylabel)
        ax.set_title(f'{title}: {ylabel}')
        ax.legend()
        ax.grid(alpha=0.25)
    save_plot(filename)


def main():
    seed_everything()
    df = pd.read_csv(DATA)
    assert 'Outcome' in df.columns and len(df.columns) == 9

    # 7.1.1: tabla descriptiva y distribución original.
    summary = pd.DataFrame({'columna': df.columns, 'tipo': df.dtypes.astype(str).values,
                            'NaN_original': df.isna().sum().values})
    summary['filas_dataset'] = len(df)
    summary['variables_predictoras'] = 8
    summary['variable_objetivo'] = 'Outcome'
    summary.to_csv(OUT / '7_1_1_resumen.csv', index=False)
    distribution = df['Outcome'].value_counts().sort_index()
    distribution.rename_axis('Outcome').reset_index(name='conteo').to_csv(
        OUT / '7_1_1_clases.csv', index=False)
    plt.figure(figsize=(6, 4))
    bars = plt.bar(['Outcome=0', 'Outcome=1'], distribution.values)
    for bar, n in zip(bars, distribution.values):
        plt.text(bar.get_x() + bar.get_width()/2, n + 4,
                 f'{n} ({100*n/len(df):.1f}%)', ha='center')
    plt.title('7.1.1 Distribución de Outcome')
    plt.xlabel('Clase')
    plt.ylabel('Pacientes')
    save_plot('7_1_1_clases.png')

    # 7.1.2: los ceros inválidos pasan a NaN antes de dividir.
    x = df.drop(columns='Outcome').copy()
    x[INVALID_ZERO] = x[INVALID_ZERO].replace(0, np.nan)
    y = df['Outcome'].astype(int)
    x.isna().sum().rename('NaN_tras_ceros_invalidos').to_csv(
        OUT / '7_1_2_faltantes.csv')
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=SEED)

    # 7.2: arquitectura, parámetros y épocas configuradas.
    arch_rows = []
    for label, hidden in ARCHITECTURES.items():
        model = MLP(hidden)
        arch_rows.append({'arquitectura': label, 'capas': f'8 -> {" -> ".join(map(str, hidden))} -> 1',
                          'parametros': sum(p.numel() for p in model.parameters()),
                          'batch_size': BATCH_SIZE, 'epocas_maximas': EPOCHS,
                          'activacion_oculta': 'ReLU', 'salida': 'Sigmoide'})
    pd.DataFrame(arch_rows).to_csv(OUT / '7_2_1_arquitecturas.csv', index=False)

    # 7.3.1: selección exclusivamente en training mediante CV.
    all_cv = []
    for label, hidden in ARCHITECTURES.items():
        all_cv.append(cv_experiment(x_train, y_train, hidden, 'Ninguna', label))
    base_cv = pd.concat(all_cv, ignore_index=True)
    best_arch = (base_cv.groupby('configuracion')['ROC_AUC'].mean().idxmax())
    hidden = ARCHITECTURES[best_arch]
    for strategy in ['L1', 'L2', 'Dropout 0.2', 'Early stopping']:
        all_cv.append(cv_experiment(x_train, y_train, hidden, strategy,
                                    f'{best_arch} + {strategy}'))
    cv_results = pd.concat(all_cv, ignore_index=True)
    cv_results.to_csv(OUT / '7_3_3_cv_por_fold.csv', index=False)
    cv_summary = cv_results.groupby('configuracion').agg(
        F1_media=('F1', 'mean'), F1_desviacion=('F1', 'std'),
        ROC_AUC_media=('ROC_AUC', 'mean'), ROC_AUC_desviacion=('ROC_AUC', 'std'))
    cv_summary.to_csv(OUT / '7_3_3_comparacion_cv.csv')
    print('\nResultados CV:\n', cv_summary.to_string())

    # Selección de la estrategia sobre la arquitectura previamente elegida.
    candidates = ['Ninguna', 'L1', 'L2', 'Dropout 0.2', 'Early stopping']
    selected_strategy = max(candidates, key=lambda s: cv_summary.loc[
        best_arch if s == 'Ninguna' else f'{best_arch} + {s}', 'ROC_AUC_media'])

    # 7.3.2: curvas con validación interna solo dentro de training.
    x_fit, x_val, y_fit, y_val = train_test_split(
        x_train, y_train, test_size=0.2, stratify=y_train, random_state=SEED)
    prep_inner = preprocessing()
    xi_fit = prep_inner.fit_transform(x_fit)
    xi_val = prep_inner.transform(x_val)
    for label, h in ARCHITECTURES.items():
        _, history = train_network(xi_fit, y_fit.to_numpy(), xi_val, y_val.to_numpy(), h)
        history.to_csv(OUT / f'7_3_2_curvas_{label.replace(",", "_").replace("[", "").replace("]", "")}.csv', index=False)
        plot_curves(history, f'7_3_2_curvas_{label.replace(",", "_").replace("[", "").replace("]", "")}.png', label)
    for strategy in candidates:
        _, history = train_network(xi_fit, y_fit.to_numpy(), xi_val, y_val.to_numpy(), hidden, strategy)
        safe = strategy.replace(' ', '_')
        history.to_csv(OUT / f'7_3_2_regularizacion_{safe}.csv', index=False)
        plot_curves(history, f'7_3_2_regularizacion_{safe}.png', f'{best_arch} + {strategy}')

    # 7.4: entrenamiento final sin consultar testing durante ajuste.
    # Para early stopping se reserva validación interna del training.
    if selected_strategy == 'Early stopping':
        final_prep = preprocessing()
        x_final_fit = final_prep.fit_transform(x_fit)
        x_final_val = final_prep.transform(x_val)
        model, final_history = train_network(x_final_fit, y_fit.to_numpy(),
                                             x_final_val, y_val.to_numpy(),
                                             hidden, selected_strategy)
    else:
        final_prep = preprocessing()
        x_final_fit = final_prep.fit_transform(x_train)
        # Entrenamiento completo: no usar test ni un validation set para modificar pesos.
        seed_everything()
        model = MLP(hidden, dropout=0.2 if selected_strategy == 'Dropout 0.2' else 0)
        optimizer = torch.optim.Adam(model.parameters(), lr=LR,
                                     weight_decay=0.001 if selected_strategy == 'L2' else 0)
        xx = torch.as_tensor(x_final_fit, dtype=torch.float32)
        yy = torch.as_tensor(y_train.to_numpy(), dtype=torch.float32)
        for epoch in range(EPOCHS):
            model.train()
            generator = torch.Generator().manual_seed(SEED + epoch)
            for batch in torch.randperm(len(yy), generator=generator).split(BATCH_SIZE):
                optimizer.zero_grad()
                loss = nn.functional.binary_cross_entropy_with_logits(model(xx[batch]), yy[batch])
                if selected_strategy == 'L1':
                    loss += 0.0001 * sum(p.abs().sum() for p in model.parameters())
                loss.backward()
                optimizer.step()
    x_test_processed = final_prep.transform(x_test)
    _, _, prob = evaluate(model, x_test_processed, y_test.to_numpy())
    metrics = scores(y_test.to_numpy(), prob)
    pd.DataFrame([{'arquitectura': best_arch, 'regularizacion': selected_strategy,
                   **metrics}]).to_csv(OUT / '7_4_2_metricas_testing.csv', index=False)
    print('\nSelección:', best_arch, selected_strategy)
    print('Testing (una sola evaluación):', metrics)

    cm = confusion_matrix(y_test, prob >= 0.5)
    ConfusionMatrixDisplay(cm, display_labels=['Outcome=0', 'Outcome=1']).plot(cmap='Blues')
    plt.title('7.4.2 Matriz de confusión - testing')
    save_plot('7_4_2_matriz_confusion.png')
    plt.figure(figsize=(7, 4.5))
    for cls in [0, 1]:
        plt.hist(prob[y_test.to_numpy() == cls], bins=18, alpha=0.6,
                 label=f'Clase real {cls}')
    plt.axvline(0.5, color='black', linestyle='--', label='Umbral 0.5')
    plt.title('7.4.2 Probabilidades estimadas por clase real')
    plt.xlabel('Probabilidad estimada de Outcome=1')
    plt.ylabel('Frecuencia')
    plt.legend()
    save_plot('7_4_2_probabilidades.png')

    # Evidencia para interpretación sin afirmar sobreajuste/subajuste sin observar las curvas.
    with open(OUT / '7_4_2_guia_interpretacion.txt', 'w', encoding='utf-8') as f:
        f.write(f'Arquitectura seleccionada por CV: {best_arch}\n')
        f.write(f'Regularización seleccionada por CV: {selected_strategy}\n')
        f.write(f'Métricas testing: {metrics}\n\n')
        f.write('Sobreajuste: señalar una curva donde loss de training siga bajando mientras '
                'loss de validación aumente, si ocurre.\n')
        f.write('Subajuste: señalar una curva donde ambos losses sean altos o las accuracies '
                'se mantengan bajas y próximas, si ocurre. No atribuirlos sin evidencia.\n')
    print(f'\nResultados guardados en: {OUT}')


if __name__ == '__main__':
    main()
