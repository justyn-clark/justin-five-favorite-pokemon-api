const express = require('express');
const axios = require('axios');
const statistics = require('simple-statistics');
const app = express();

app.get('/justin-five-favorite-pokemon', (req, res) => {
  const pokemonNames = ["ditto", "golem", "exeggutor", "pikachu", "chikorita"];
  let pokemonDataList = [];
  let baseHappiness = [];

  Promise.all(pokemonNames.map(async (name) => {
    try {
      const pokemonResponse = await axios.get(`https://pokeapi.co/api/v2/pokemon/${name}`);
      const { name:pokemonName, height, weight, moves } = pokemonResponse.data;
      const shuffledArray = moves.sort(() => 0.5 - Math.random());
      const limitedMoves = shuffledArray.slice(0,2);
      const speciesResponse = await axios.get(`https://pokeapi.co/api/v2/pokemon-species/${pokemonResponse.data["id"]}`);
      const color = speciesResponse.data["color"]["name"]
      const happiness = speciesResponse.data["base_happiness"]
      baseHappiness.push(happiness);
      pokemonDataList.push({'name':pokemonName,'height':height, 'weight':weight, 'moves':limitedMoves, 'color':color, 'base_happiness':happiness});
    } catch (err) {
      console.error(err);
    }
  })).then(() => {
    let average = baseHappiness.reduce((a, b) => a + b, 0) / baseHappiness.length;
    let mean = statistics.mean(baseHappiness);
    let median = statistics.median(baseHappiness);
    res.json({pokemonDataList, average, mean, median});
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});
