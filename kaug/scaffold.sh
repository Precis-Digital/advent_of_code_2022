#!/bin/bash
DAY=$1

echo "Creating Boilerplate for day ${DAY}"
cp boilerplate/day.txt boilerplate/day${DAY}.txt
sed -i "s/{DAY}/${DAY}/g" boilerplate/day${DAY}.txt
mv -i boilerplate/day${DAY}.txt src/solutions/day${DAY}.rs


INPUT_URL="https://adventofcode.com/2022/day/${DAY}/input"
TEMP_INPUT="temp.txt"
curl "${INPUT_URL}" -H "cookie: session=$AOC_SESSION_COOKIE" -o "${TEMP_INPUT}" 2>/dev/null
mv -i ${TEMP_INPUT} input/day${DAY}.txt 