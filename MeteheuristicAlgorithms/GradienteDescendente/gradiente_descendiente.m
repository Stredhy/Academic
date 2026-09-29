% =========================================================================
% Algoritmo: Gradiente Descendiente 2D
% Asignatura: Algoritmos Metaheurísticos - CUCEI

% Nombre: Eric Oswaldo Aguilar Nova
% Codigo: 219635295

% =========================================================================

clc; clear; close all;

% -------------------------------------------------------------------------
% 1. Definición de la Función Objetivo y su Gradiente
% -------------------------------------------------------------------------
% Función: f(x1, x2) = x1^2 + 2*x2^2
f = @(x1, x2) x1.^2 + 2*x2.^2;

% Gradiente: [df/dx1; df/dx2] = [2*x1; 4*x2]
grad_f = @(x) [2*x(1); 4*x(2)];

% -------------------------------------------------------------------------
% 2. Hiperparámetros y Condiciones Iniciales
% -------------------------------------------------------------------------
alpha = 0.1;           % Tasa de aprendizaje (learning rate)
max_iter = 50;         % Número máximo de iteraciones
tol = 1e-5;            % Tolerancia de convergencia en el gradiente

x_start = [4; 4];      % Punto inicial de búsqueda [x1; x2]

% Vector para guardar el historial de la trayectoria
path = zeros(2, max_iter + 1);
path(:, 1) = x_start;

% -------------------------------------------------------------------------
% 3. Bucle Principal de Optimización
% -------------------------------------------------------------------------
x_curr = x_start;
iter_realizadas = max_iter;

for k = 1:max_iter
    % A. Calcular el gradiente en el punto actual
    g = grad_f(x_curr);
    
    % B. Criterio de paro: Si la norma del gradiente es casi cero, detiene
    if norm(g) < tol
        iter_realizadas = k - 1;
        path = path(:, 1:k);
        fprintf('Convergencia alcanzada en la iteración %d.\n', iter_realizadas);
        break;
    end
    
    % C. Regla de actualización: x^(k+1) = x^(k) - alpha * grad(f)
    x_next = x_curr - alpha * g;
    
    % D. Guardar estado y actualizar punto actual
    path(:, k + 1) = x_next;
    x_curr = x_next;
end

% Mostrar resultados en consola
fprintf('Punto final obtenido: (x1, x2) = (%.5f, %.5f)\n', x_curr(1), x_curr(2));
fprintf('Valor mínimo f(x): %.6f\n', f(x_curr(1), x_curr(2)));

% -------------------------------------------------------------------------
% 4. Visualización Gráfica
% -------------------------------------------------------------------------
[X1, X2] = meshgrid(-5:0.1:5, -5:0.1:5);
Z = f(X1, X2);

figure('Name', 'Gradiente Descendiente - CUCEI', 'Color', 'w');
contour(X1, X2, Z, 30, 'LineWidth', 1.2);
hold on;
colorbar;

% Graficar trayectoria
plot(path(1, :), path(2, :), 'r-o', 'LineWidth', 1.8, 'MarkerFaceColor', 'r', 'MarkerSize', 4);
plot(x_start(1), x_start(2), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 8); % Inicio
plot(x_curr(1), x_curr(2), 'bx', 'LineWidth', 2.5, 'MarkerSize', 10);        % Mínimo hallado

title('Trayectoria del Gradiente Descendiente - {NOMBRE}');
xlabel('x_1');
ylabel('x_2');
legend('Curvas de Nivel f(x)', 'Ruta de optimización', 'Punto Inicial', 'Mínimo Encontrado');
grid on;
axis equal;