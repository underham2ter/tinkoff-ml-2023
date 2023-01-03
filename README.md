Суть моего решения состоит в том, чтобы, для определения списывания,
рассмотреть изменения в общей структуре кода, а не изменения в названиях переменных или функицй.
Ведь в ходе копирования именно их и меняет ленивый студент, стараясь избежать подозрений.
Структуру кода при этом он меняет мало: удаляет или вставляет компоненты, меняет их местами.
Поэтому в моем решении используется измененный алгоритм Левенштайна, позволяющий учесть перестановку
cоседей двух последовательностей (алг. Дамерау — Левенштейна).

Конечный балл (score) выставляется по формуле:
1 - Расстояние/max(Длина первой последовательности, Длина второй последовательности)
