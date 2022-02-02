/* -----------------------------------------------------------
Course: CSE 251
Lesson Week: 12
File: team1.go

Purpose: Process URLs

Instructions:

Part 1
- Take this program and use goroutines for the function getPerson().

Part 2
- Create a function "getSpecies()" that will receive the following urls
  using that function as a goroutine.
- For a species, display name, average_height and language

"http://swapi.dev/api/species/1/",
"http://swapi.dev/api/species/2/",
"http://swapi.dev/api/species/3/",
"http://swapi.dev/api/species/6/",
"http://swapi.dev/api/species/15/",
"http://swapi.dev/api/species/19/",
"http://swapi.dev/api/species/20/",
"http://swapi.dev/api/species/23/",
"http://swapi.dev/api/species/24/",
"http://swapi.dev/api/species/25/",
"http://swapi.dev/api/species/26/",
"http://swapi.dev/api/species/27/",
"http://swapi.dev/api/species/28/",
"http://swapi.dev/api/species/29/",
"http://swapi.dev/api/species/30/",
"http://swapi.dev/api/species/33/",
"http://swapi.dev/api/species/34/",
"http://swapi.dev/api/species/35/",
"http://swapi.dev/api/species/36/",
"http://swapi.dev/api/species/37/",

----------------------------------------------------------- */
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

type Person struct {
	Birth_year string
	Created    time.Time
	Edited     time.Time
	Eye_color  string
	Films      []string
	Gender     string
	Hair_color string
	Height     string
	Homeworld  string
	Mass       string
	Name       string
	Skin_color string
	Species    []string
	Starships  []string
	Url        string
	Vehicles   []string
}

type Species struct {
	Name            string    `json:"name"`
	Classification  string    `json:"classification"`
	Designation     string    `json:"designation"`
	AverageHeight   string    `json:"average_height"`
	SkinColors      string    `json:"skin_colors"`
	HairColors      string    `json:"hair_colors"`
	EyeColors       string    `json:"eye_colors"`
	AverageLifespan string    `json:"average_lifespan"`
	Homeworld       string    `json:"homeworld"`
	Language        string    `json:"language"`
	People          []string  `json:"people"`
	Films           []string  `json:"films"`
	Created         time.Time `json:"created"`
	Edited          time.Time `json:"edited"`
	URL             string    `json:"url"`
}

func getPerson(url string, wg *sync.WaitGroup) {
	// make a sample HTTP GET request
	res, err := http.Get(url)

	// check for response error
	if err != nil {
		log.Fatal(err)
	}

	// read all response body
	data, _ := ioutil.ReadAll(res.Body)

	// close response body
	res.Body.Close()

	// fmt.Println(string(data))

	person := Person{}
	jsonErr := json.Unmarshal(data, &person)
	if jsonErr != nil {
		log.Fatal(jsonErr)
		fmt.Println("ERROR Pasing the JSON")
	}

	fmt.Println("-----------------------------------------------")
	// fmt.Println(person)
	fmt.Println("Name      : ", person.Name)
	fmt.Println("Birth     : ", person.Birth_year)
	fmt.Println("Eye color : ", person.Eye_color)

	wg.Done()
}

func getSpecies(url string, wg *sync.WaitGroup) {
	// make a sample HTTP GET request
	res, err := http.Get(url)

	// check for response error
	if err != nil {
		log.Fatal(err)
	}

	// read all response body
	data, _ := ioutil.ReadAll(res.Body)

	// close response body
	res.Body.Close()

	// fmt.Println(string(data))

	species := Species{}
	jsonErr := json.Unmarshal(data, &species)
	if jsonErr != nil {
		log.Fatal(jsonErr)
		fmt.Println("ERROR Pasing the JSON")
	}

	fmt.Println("-----------------------------------------------")
	// fmt.Println(person)
	fmt.Println("Name           : ", species.Name)
	fmt.Println("Average Height : ", species.AverageHeight)
	fmt.Println("Language       : ", species.Language)

	wg.Done()
}

func main() {
	urls := []string{
		"http://swapi.dev/api/people/1/",
		"http://swapi.dev/api/people/2/",
		"http://swapi.dev/api/people/3/",
		"http://swapi.dev/api/people/4/",
		"http://swapi.dev/api/people/5/",
		"http://swapi.dev/api/people/6/",
		"http://swapi.dev/api/people/7/",
		"http://swapi.dev/api/people/8/",
		"http://swapi.dev/api/people/9/",
		"http://swapi.dev/api/people/10/",
		"http://swapi.dev/api/people/12/",
		"http://swapi.dev/api/people/13/",
		"http://swapi.dev/api/people/14/",
		"http://swapi.dev/api/people/15/",
		"http://swapi.dev/api/people/16/",
		"http://swapi.dev/api/people/18/",
		"http://swapi.dev/api/people/19/",
		"http://swapi.dev/api/people/81/",
	}

	species_urls := []string{
		"http://swapi.dev/api/species/1/",
		"http://swapi.dev/api/species/2/",
		"http://swapi.dev/api/species/3/",
		"http://swapi.dev/api/species/6/",
		"http://swapi.dev/api/species/15/",
		"http://swapi.dev/api/species/19/",
		"http://swapi.dev/api/species/20/",
		"http://swapi.dev/api/species/23/",
		"http://swapi.dev/api/species/24/",
		"http://swapi.dev/api/species/25/",
		"http://swapi.dev/api/species/26/",
		"http://swapi.dev/api/species/27/",
		"http://swapi.dev/api/species/28/",
		"http://swapi.dev/api/species/29/",
		"http://swapi.dev/api/species/30/",
		"http://swapi.dev/api/species/33/",
		"http://swapi.dev/api/species/34/",
		"http://swapi.dev/api/species/35/",
		"http://swapi.dev/api/species/36/",
		"http://swapi.dev/api/species/37/",
	}
	// ch := make(chan Person, len(urls))
	wg1 := &sync.WaitGroup{}
	wg2 := &sync.WaitGroup{}

	wg1.Add(len(urls))
	for _, url := range urls {
		go getPerson(url, wg1)
	}
	wg1.Wait()

	wg2.Add(len(species_urls))
	for _, url := range species_urls {
		go getSpecies(url, wg2)
	}

	wg2.Wait()

	fmt.Println("All done!")
}
