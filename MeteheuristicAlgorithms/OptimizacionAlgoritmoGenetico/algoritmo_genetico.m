% =========================================================================
% Algoritmo: Algoritmo Evolutivo Básico (GA Continuo / Real)
% Asignatura: Algoritmos Metaheurísticos - CUCEI
% Objetivo: Minimizar f(x1, x2) = x1^2 + 2*x2^2
% =========================================================================

clc; clear; close all;

% 1. Parámetros del Algoritmo Evolutivo
num_pop = 30;         % Tamaño de la población
num_gen = 50;          % Número de generaciones
p_cross = 0.8;         % Probabilidad de cruza
p_mut = 0.15;          % Probabilidad de mutación
mut_sigma = 0.3;       % Desviación estándar del paso de mutación gaussiana
bounds = [-5, 5];      % Límites del espacio de búsqueda [x_min, x_max]

% Función Objetivo (Minimización)
f = @(x1, x2) x1.^2 + 2*x2.^2;

% 2. Inicialización Aleatoria de la Población (Matriz de num_pop x 2)
pop = bounds(1) + (bounds(2) - bounds(1)) * rand(num_pop, 2);
best_history = zeros(num_gen, 1);

% 3. Ciclo Evolutivo Principal
for gen = 1:num_gen
    % A. Evaluación de la Aptitud (Fitness)
    obj_vals = f(pop(:, 1), pop(:, 2));
    fitness = 1 ./ (1 + obj_vals);

    % Almacenar la mejor solución alcanzada
    [~, best_idx] = max(fitness);
    best_sol = pop(best_idx, :);
    best_history(gen) = obj_vals(best_idx);

    % B. Selección por Torneo (Tamaño = 2)
    new_pop = zeros(num_pop, 2);
    for i = 1:num_pop
        i1 = randi(num_pop);
        i2 = randi(num_pop);
        if fitness(i1) > fitness(i2)
            new_pop(i, :) = pop(i1, :);
        else
            new_pop(i, :) = pop(i2, :);
        end
    end
    
    % C. Operador de Cruza Aritmética
    for i = 1:2:num_pop-1
        if rand() < p_cross
            alpha = rand();
            parent1 = new_pop(i, :);
            parent2 = new_pop(i+1, :);
            new_pop(i, :)   = alpha * parent1 + (1 - alpha) * parent2;
            new_pop(i+1, :) = alpha * parent2 + (1 - alpha) * parent1;
        end
    end

    % D. Operador de Mutación Gaussiana
    for i = 1:num_pop
        if rand() < p_mut
            new_pop(i, :) = new_pop(i, :) + mut_sigma * randn(1, 2);
            % Control de bordes (mantener dentro del dominio)
            new_pop(i, :) = max(min(new_pop(i, :), bounds(2)), bounds(1));
        end
    end

    % E. Elitismo: Preservar al mejor individuo de la generación previa
    new_pop(1, :) = best_sol;
    pop = new_pop;
end

% Resultados finales en consola
fprintf('Mejor solución encontrada: (x1, x2) = (%.5f, %.5f)\n', best_sol(1), best_sol(2));
fprintf('Valor mínimo f(x): %.6f\n', f(best_sol(1), best_sol(2)));

% 4. Visualización de la Convergencia
figure('Name', 'Algoritmo Evolutivo - CUCEI', 'Color', 'w');
plot(1:num_gen, best_history, 'b-o', 'LineWidth', 1.8, 'MarkerFaceColor', 'b');
xlabel('Generación'); ylabel('Mejor Valor f(x)');
title('Curva de Convergencia del Algoritmo Evolutivo');
grid on;