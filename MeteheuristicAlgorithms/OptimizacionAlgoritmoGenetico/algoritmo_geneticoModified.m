% =========================================================================
% Algoritmo: Algoritmo Evolutivo Básico (GA Continuo / Real)
% Asignatura: Algoritmos Metaheurísticos - CUCEI
%
% Funciones:
%   1. Rastrigin  - Prueba de Multimodalidad
%   2. Rosenbrock - Prueba de Explotación en Valles Plano-Curvos
%
% Cada función se ejecuta 10 veces.
% =========================================================================

clc;
clear;
close all;

% Número de ejecuciones por función
num_runs = 10;


%% ========================================================================
%                         FUNCIÓN DE RASTRIGIN
% =========================================================================
%
% f(x1,x2) = 20 + x1^2 + x2^2
%            - 10(cos(2*pi*x1) + cos(2*pi*x2))
%
% Mínimo global:
% f(0,0) = 0
%
% Dominio:
% x1,x2 ∈ [-5.12, 5.12]
% =========================================================================

fprintf('\n============================================================\n');
fprintf('                    FUNCIÓN DE RASTRIGIN\n');
fprintf('============================================================\n');

% Hiperparámetros para Rastrigin
num_pop = 40;
num_gen = 150;
p_cross = 0.8;
p_mut = 0.20;
mut_sigma = 0.20;

% Límites de Rastrigin
bounds = [-5.12, 5.12];

% Función objetivo
f = @(x1, x2) 20 + x1.^2 + x2.^2 ...
    - 10 * (cos(2*pi*x1) + cos(2*pi*x2));


% Matriz para guardar resultados
resultados_rastrigin = zeros(num_runs, 5);

% Matriz para guardar las curvas de convergencia
historias_rastrigin = zeros(num_gen, num_runs);


for run = 1:num_runs

    % ---------------------------------------------------------------
    % Inicialización de la población
    % ---------------------------------------------------------------
    pop = bounds(1) + (bounds(2) - bounds(1)) * rand(num_pop, 2);

    best_history = zeros(num_gen, 1);


    % ---------------------------------------------------------------
    % Ciclo Evolutivo Principal
    % ---------------------------------------------------------------
    for gen = 1:num_gen

        % A. Evaluación
        obj_vals = f(pop(:,1), pop(:,2));

        % Fitness para minimización
        fitness = 1 ./ (1 + obj_vals);

        % Mejor individuo de la generación
        [~, best_idx] = max(fitness);

        best_sol = pop(best_idx,:);
        best_value = obj_vals(best_idx);

        % Guardar mejor valor
        best_history(gen) = best_value;


        % -----------------------------------------------------------
        % B. Selección por torneo
        % -----------------------------------------------------------
        new_pop = zeros(num_pop, 2);

        for i = 1:num_pop

            i1 = randi(num_pop);
            i2 = randi(num_pop);

            if fitness(i1) > fitness(i2)
                new_pop(i,:) = pop(i1,:);
            else
                new_pop(i,:) = pop(i2,:);
            end

        end


        % -----------------------------------------------------------
        % C. Cruza aritmética
        % -----------------------------------------------------------
        for i = 1:2:num_pop-1

            if rand() < p_cross

                alpha = rand();

                parent1 = new_pop(i,:);
                parent2 = new_pop(i+1,:);

                new_pop(i,:) = ...
                    alpha * parent1 + (1-alpha) * parent2;

                new_pop(i+1,:) = ...
                    alpha * parent2 + (1-alpha) * parent1;

            end

        end


        % -----------------------------------------------------------
        % D. Mutación gaussiana
        % -----------------------------------------------------------
        for i = 1:num_pop

            if rand() < p_mut

                new_pop(i,:) = new_pop(i,:) ...
                    + mut_sigma * randn(1,2);

                % Mantener dentro de los límites
                new_pop(i,:) = max( ...
                    min(new_pop(i,:), bounds(2)), ...
                    bounds(1));

            end

        end


        % -----------------------------------------------------------
        % E. Elitismo
        % -----------------------------------------------------------
        new_pop(1,:) = best_sol;

        pop = new_pop;

    end


    % ---------------------------------------------------------------
    % Obtener resultado final de la ejecución
    % ---------------------------------------------------------------
    [min_value, min_gen] = min(best_history);

    % Mejor solución asociada al mínimo
    obj_vals = f(pop(:,1), pop(:,2));
    [~, best_idx] = min(obj_vals);

    final_sol = pop(best_idx,:);

    % Valor con el que inició la gráfica
    initial_value = best_history(1);

    % Guardar resultados
    resultados_rastrigin(run,:) = ...
        [final_sol(1), final_sol(2), min_value, ...
         initial_value, min_gen];

    historias_rastrigin(:,run) = best_history;


    % ---------------------------------------------------------------
    % Mostrar resultados
    % ---------------------------------------------------------------
    fprintf('\nEjecución %d:\n', run);

    fprintf('  Mejor solución: (x1, x2) = (%.5f, %.5f)\n', ...
        final_sol(1), final_sol(2));

    fprintf('  Valor mínimo encontrado: %.8f\n', min_value);

    fprintf('  Valor inicial de la gráfica: %.8f\n', ...
        initial_value);

    fprintf('  Generación del mínimo: %d\n', min_gen);

end


%% ========================================================================
%                         RESULTADOS RASTRIGIN
% =========================================================================

fprintf('\n------------------------------------------------------------\n');
fprintf('RESUMEN RASTRIGIN\n');
fprintf('------------------------------------------------------------\n');

fprintf('Mínimo global esperado: f(0,0) = 0\n\n');

fprintf(' Ejecución       x1          x2       Mínimo       Inicial    Gen.\n');
fprintf('------------------------------------------------------------------\n');

for run = 1:num_runs

    fprintf('     %2d       %8.5f   %8.5f   %10.8f   %10.6f   %3d\n', ...
        run, ...
        resultados_rastrigin(run,1), ...
        resultados_rastrigin(run,2), ...
        resultados_rastrigin(run,3), ...
        resultados_rastrigin(run,4), ...
        resultados_rastrigin(run,5));

end


%% ========================================================================
%                         GRÁFICA RASTRIGIN
% =========================================================================

figure('Name','Convergencia - Rastrigin','Color','w');

plot(historias_rastrigin, 'LineWidth', 1.2);

xlabel('Generación');
ylabel('Mejor valor f(x)');
title('Convergencia del Algoritmo Genético - Rastrigin');

grid on;

legend('Ejecución 1','Ejecución 2','Ejecución 3', ...
       'Ejecución 4','Ejecución 5','Ejecución 6', ...
       'Ejecución 7','Ejecución 8','Ejecución 9', ...
       'Ejecución 10', ...
       'Location','northeast');


%% ========================================================================
%                         FUNCIÓN DE ROSENBROCK
% =========================================================================
%
% f(x1,x2) = 100(x2 - x1^2)^2 + (1-x1)^2
%
% Mínimo global:
% f(1,1) = 0
%
% Dominio:
% x1,x2 ∈ [-2,2]
% =========================================================================

fprintf('\n\n============================================================\n');
fprintf('                   FUNCIÓN DE ROSENBROCK\n');
fprintf('============================================================\n');


% Hiperparámetros para Rosenbrock
num_pop = 50;
num_gen = 200;
p_cross = 0.9;
p_mut = 0.20;
mut_sigma = 0.08;

% Límites de Rosenbrock
bounds = [-2, 2];

% Función objetivo
f = @(x1, x2) 100*(x2 - x1.^2).^2 + (1-x1).^2;


% Matriz para guardar resultados
resultados_rosenbrock = zeros(num_runs, 5);

% Matriz para guardar curvas
historias_rosenbrock = zeros(num_gen, num_runs);


for run = 1:num_runs

    % ---------------------------------------------------------------
    % Inicialización
    % ---------------------------------------------------------------
    pop = bounds(1) + (bounds(2) - bounds(1)) * rand(num_pop, 2);

    best_history = zeros(num_gen, 1);


    % ---------------------------------------------------------------
    % Ciclo Evolutivo
    % ---------------------------------------------------------------
    for gen = 1:num_gen

        % A. Evaluación
        obj_vals = f(pop(:,1), pop(:,2));

        fitness = 1 ./ (1 + obj_vals);

        [~, best_idx] = max(fitness);

        best_sol = pop(best_idx,:);
        best_value = obj_vals(best_idx);

        best_history(gen) = best_value;


        % -----------------------------------------------------------
        % B. Selección por torneo
        % -----------------------------------------------------------
        new_pop = zeros(num_pop, 2);

        for i = 1:num_pop

            i1 = randi(num_pop);
            i2 = randi(num_pop);

            if fitness(i1) > fitness(i2)
                new_pop(i,:) = pop(i1,:);
            else
                new_pop(i,:) = pop(i2,:);
            end

        end


        % -----------------------------------------------------------
        % C. Cruza aritmética
        % -----------------------------------------------------------
        for i = 1:2:num_pop-1

            if rand() < p_cross

                alpha = rand();

                parent1 = new_pop(i,:);
                parent2 = new_pop(i+1,:);

                new_pop(i,:) = ...
                    alpha * parent1 + (1-alpha) * parent2;

                new_pop(i+1,:) = ...
                    alpha * parent2 + (1-alpha) * parent1;

            end

        end


        % -----------------------------------------------------------
        % D. Mutación gaussiana
        % -----------------------------------------------------------
        for i = 1:num_pop

            if rand() < p_mut

                new_pop(i,:) = new_pop(i,:) ...
                    + mut_sigma * randn(1,2);

                % Mantener dentro del dominio
                new_pop(i,:) = max( ...
                    min(new_pop(i,:), bounds(2)), ...
                    bounds(1));

            end

        end


        % -----------------------------------------------------------
        % E. Elitismo
        % -----------------------------------------------------------
        new_pop(1,:) = best_sol;

        pop = new_pop;

    end


    % ---------------------------------------------------------------
    % Resultado final
    % ---------------------------------------------------------------
    [min_value, min_gen] = min(best_history);

    obj_vals = f(pop(:,1), pop(:,2));

    [~, best_idx] = min(obj_vals);

    final_sol = pop(best_idx,:);

    initial_value = best_history(1);


    % Guardar resultados
    resultados_rosenbrock(run,:) = ...
        [final_sol(1), final_sol(2), min_value, ...
         initial_value, min_gen];

    historias_rosenbrock(:,run) = best_history;


    % ---------------------------------------------------------------
    % Mostrar resultados
    % ---------------------------------------------------------------
    fprintf('\nEjecución %d:\n', run);

    fprintf('  Mejor solución: (x1, x2) = (%.5f, %.5f)\n', ...
        final_sol(1), final_sol(2));

    fprintf('  Valor mínimo encontrado: %.8f\n', min_value);

    fprintf('  Valor inicial de la gráfica: %.8f\n', ...
        initial_value);

    fprintf('  Generación del mínimo: %d\n', min_gen);

end


%% ========================================================================
%                       RESULTADOS ROSENBROCK
% =========================================================================

fprintf('\n------------------------------------------------------------\n');
fprintf('RESUMEN ROSENBROCK\n');
fprintf('------------------------------------------------------------\n');

fprintf('Mínimo global esperado: f(1,1) = 0\n\n');

fprintf(' Ejecución       x1          x2       Mínimo       Inicial    Gen.\n');
fprintf('------------------------------------------------------------------\n');

for run = 1:num_runs

    fprintf('     %2d       %8.5f   %8.5f   %10.8f   %10.6f   %3d\n', ...
        run, ...
        resultados_rosenbrock(run,1), ...
        resultados_rosenbrock(run,2), ...
        resultados_rosenbrock(run,3), ...
        resultados_rosenbrock(run,4), ...
        resultados_rosenbrock(run,5));

end


%% ========================================================================
%                       GRÁFICA ROSENBROCK
% =========================================================================

figure('Name','Convergencia - Rosenbrock','Color','w');

plot(historias_rosenbrock, 'LineWidth', 1.2);

xlabel('Generación');
ylabel('Mejor valor f(x)');
title('Convergencia del Algoritmo Genético - Rosenbrock');

grid on;

legend('Ejecución 1','Ejecución 2','Ejecución 3', ...
       'Ejecución 4','Ejecución 5','Ejecución 6', ...
       'Ejecución 7','Ejecución 8','Ejecución 9', ...
       'Ejecución 10', ...
       'Location','northeast');


%% ========================================================================
%                            FIN
% =========================================================================

fprintf('\n\n============================================================\n');
fprintf('                    PROCESO TERMINADO\n');
fprintf('============================================================\n');