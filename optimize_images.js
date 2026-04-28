// Оптимизация изображений для быстрой загрузки
// Используем TinyPNG API или сжимаем локально

const fs = require('fs');
const path = require('path');

console.log('Для оптимизации картинок:');
console.log('1. Иди на https://tinypng.com/');
console.log('2. Загрузи все JPG из папки images/');
console.log('3. Скачай оптимизированные');
console.log('4. Замени старые файлы');
console.log('');
console.log('Или используй команду:');
console.log('npm install -g imagemin-cli');
console.log('imagemin images/*.jpg --out-dir=images/ --plugin=mozjpeg');
