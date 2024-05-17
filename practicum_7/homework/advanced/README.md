# Предназначение каждого файла

## 1) **testing_np_linalg_eig.ipynb**
>  Во время тестрирования своих алгоритмов, я построил график который показывал величину найденного собственного числа в соответстивии с его индексом. Была замечени странность - несколько чисел были в 1000-10000 раз больше всех остальных собственных чисел на практически любой исследуемой матрицей. Посоветовавшись с Дегятревым А.Б. и Утешевым А.Ю., я решил перепроверить правильность написания кода. Действительно, несколько собственных чисел большинства матриц (заданных случайно) по модулю больше на несколько порядков всего отсального множества. Данный файл подтверждает это наблюдение.
<p float="left">
  <img src="images/image1.png" alt="Image 1" width="250" style="margin-right: 10px;" />
  <img src="images/image2.png" alt="Image 2" width="250" />
</p>

## 2) **qr_algos_battle.ipynb**
> Во время первоначального тестирования, было обнаружено, что на больших матрицах алгоритмы, которые находят сразу все собственные числа работают лучше. Поэтому я решил болле подробно изучить QR-алгоритм, основной частью которого является QR-разложение. При изучении, было обнаружено 5 разных алгоритмов QR-разложения:
> 
>   1) Стандартный алгоритм ортогонализации Грама-Шмидта - *basic_QR*
>   2) Оптимизированный алгоритм ортогонализации Грама-Шмидта (основной задачей является предотвращение потери точности при процессе вычитания $\vec{u_i} - \sum_{j=1}^i \vec{u_j}$) - *Gram_Schmidt_optimised_QR*
>   3) Оптимизированный алгоритм ортогонализации Грама-Шмидта модификации Першина А.Ю. - *qr_pershin*
>   4) Метод Хаусхолдера (метод отражений) - *qr_householder*
>   5) QR-декомпозиция с помощью вращений по Гивенсу - *qr_givens*
>

### Матрицы, на которых прогонялись алгоритмы

<p float="left">
  <img src="images/matrix_for_qr_1.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_2.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_3.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_4.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_5.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_6.png" alt="Image 1" width="200" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_7.png" alt="Image 1" width="200" style="margin-right: 10px;" />
</p>

### Результаты

<p float="left">
  <img src="images/qr_median_error_with_givens.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/qr_median_error_with_givens.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/qr_runtime_with_givens.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/qr_runtime_without_givens.png" alt="Image 1" width="300" style="margin-right: 10px;" />
</p>

#### Выводы: наиболее оптимальными по точности и скорости решения являются 2 алгоримта: *Gram_Schmidt_optimised_QR* и *qr_householder*.

## 3) **method_vault.ipynb**
> Просто файл, который содержит **все** алгоритмы которые были протестированы

### Полный список:
    1) Jacobi method for real symmetric matrix
    2) Power Iteration method with deflation
    3) Basic Gram-Schmidt process with normalization
    4) QR algorithm with shifts for real symmetric matrix
    5) QR by pershin
    6) Optimized Gram-Schmidt process with normalization
    7) QR using householder matrices
    8) QR decomposition using Givens rotations
    9) Rayleigh Quotient Iteration for symmetric matrix

## 4) **eigenvalue_search_algorithms_testing.ipynb**

> файл в котором происходит более детальный тест определенного алгоритма. Файл позволяет узнать ошибку по каждому конекретному собственному числу, сравнить значение каждого собственного числа с numpy, узнать время работы алгоритма, его медианную и среднюю ошибки.

<p float="left">
  <img src="images/hausholder_results_for_bottom_matrix.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/eig_comp_hausholder.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/eig_error_hausholder.png" alt="Image 1" width="300" style="margin-right: 10px;" />
    <img src="images/matrix_for_qr_2.png" alt="Image 1" width="300" style="margin-right: 10px;" />
</p>

# Вывод
