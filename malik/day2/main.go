package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

const DRAW = 0
const PLAYER_1_WINS = 1
const PLAYER_2_WINS = 2
const DRAW_REWARD = 3
const WIN_REWARD = 6


var CharacterToMoveMap = map[string]int{
	"A": 1,
	"B": 2,
	"C": 3,
	"X": 1,
	"Y": 2,
	"Z": 3,
}


func getScanner(fname string) (*os.File, *bufio.Scanner) {
	fmt.Println("File Name", fname)
	file, err := os.Open(fname)
	if err != nil {
		log.Fatal(err)
		file.Close()
	}

	scanner := bufio.NewScanner(file)
	return file, scanner
}


func compareHands(hand1 int, hand2 int) (int) {
	/*
	return 0 for draw
	or 1 or 2 to indicate winning hand
	*/

	if(hand1 == hand2){
		return DRAW
	}

	if(hand1 % 3) == (hand2 - 1){
		return PLAYER_2_WINS
	}
	return PLAYER_1_WINS

}

func getHandFromOutcome(player1hand, outcome int) (int) {
	/*
	return 1,2,3 indiacting hand played by player 2

	good way to think about it is that in MOD space the rotation of values looks like this
	0 = scissors
	1 = rock
	2 = paper
	3 = scissors
	4 = rock
	*/

	if (outcome == DRAW){
		return player1hand
	} else if (outcome == PLAYER_1_WINS) {
		return ((player1hand + 1) % 3) + 1
	} else {
		// player 2 wins
		return ((player1hand) % 3) + 1
	}
}

func computeScore(hand, outcome int) (int) {
	// draw
	if(outcome == DRAW){
		return hand + DRAW_REWARD
	}
	//lost
	if (outcome == PLAYER_1_WINS){
		return (hand)
	}
	// won
	return hand + WIN_REWARD
}


func solution1(scanner *bufio.Scanner) (int64) {
	var totalScore int64
	for scanner.Scan() {
		inp := scanner.Text()
		words := strings.Fields(inp)
		opponent := CharacterToMoveMap[words[0]]
		elfHand := CharacterToMoveMap[words[1]]
		winner := compareHands(opponent, elfHand)
		// fmt.Println(words, len(words))
		totalScore += int64(computeScore(elfHand, winner))
	}
	// fmt.Println("total score", totalScore)
	return totalScore
}

func solution2(scanner *bufio.Scanner) (int64) {
	var totalScore int64
	
	outcomeMap := map[string]int{
		"X": PLAYER_1_WINS,
		"Y": DRAW,
		"Z": PLAYER_2_WINS,
	}

	for scanner.Scan() {

		inp := scanner.Text()
		words := strings.Fields(inp)
		opponent := CharacterToMoveMap[words[0]]
		outcome := outcomeMap[words[1]]
		elfHand := getHandFromOutcome(opponent,outcome)
		// fmt.Println(opponent, outcome, elfHand)		
		totalScore += int64(computeScore(elfHand, outcome))
	}
	// fmt.Println("total score", totalScore)
	return totalScore
}

func main() {

    const fname = "inputs/day-2-input.txt"

    var file, scanner = getScanner(fname)
	fmt.Println("solution 1", solution1(scanner))

    file, scanner = getScanner(fname)
	fmt.Println("solution 2", solution2(scanner))

	defer file.Close()

	
	
}
