results=".results"
rep_history=".final-report/history"
report=".final-report"

# Удаляем папку с результатами, если она существует
if [ -d "$results" ]; then
    echo "Удаляем папку с результатами: $results"
    rm -rf "$results"
fi

# Запускаем тесты и сохраняем результаты
echo "Запускаем тесты..."
pytest --alluredir="$results"

# Переносим историю в результаты, если папка с историей существует
if [ -d "$rep_history" ]; then
    echo "Переносим историю в результаты: $rep_history -> $results"
    mv "$rep_history" "$results"
fi

# Удаляем отчет, если он существует
if [ -d "$report" ]; then
    echo "Удаляем отчет: $report"
    rm -rf "$report"
fi

# Генерируем отчет Allure
echo "Генерируем отчет Allure..."
allure generate "$results" -o "$report"

# Открываем сгенерированный отчет
echo "Открываем сгенерированный отчет..."
allure open "$report"