package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func main() {
	input, _ := os.Open("linn/1/input.txt")
	sc := bufio.NewScanner(input)

	elves := make([]int, 1)
	for sc.Scan() {
		if sc.Text() == "" {
			elves = append(elves, 0)
		} else {
			c, _ := strconv.ParseInt(sc.Text(), 0, 0)
			elves[len(elves)-1] += int(c)
		}
	}
	sort.Sort(sort.IntSlice(elves))
	top_elves := make([]int, 1)
	i := 1
	for i <= 3 {
		top_elves = append(top_elves, elves[len(elves)-i])
		fmt.Println(elves[len(elves)-i])
		i++
	}
}