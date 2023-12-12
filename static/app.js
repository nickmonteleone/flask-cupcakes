"use strict";

const BASE_URL = "http://localhost:5000";

const $form = $('#create-cupcake');
const $results = $('#cupcake-results');

/**
 * Get inputs from form and submit post request to create cupcake
 *
 * No inputs, use user input values from form
 * Return object with data for the added cupcake
 */

async function getCreateCupcakeData() {
  console.log('starting create cupcake');

  const body = JSON.stringify({
    'flavor': $('#flavor-input').val(),
    'size': $('#size-input').val(),
    'rating': $('#rating-input').val(),
    'image_url': $('#image_url-input').val(),
  });

  console.log('form inputs request body:', body);

  const response = await fetch(
    `${BASE_URL}/api/cupcakes`,
    {
      method: 'POST',
      body: body,
      headers: {
        "Content-Type": "application/json",
      }
    }
  );

  const cupcakeData = (await response.json()).cupcake;
  console.log('cupcake data for created object', cupcakeData);

  return cupcakeData
}


/** Conductor function to recieve form submit and show results */

async function handleSubmit(evt) {
  evt.preventDefault();
  console.log('event for form submit:', evt)

  const createdCupcakeData = await getCreateCupcakeData();
  console.log('create cupcake result:', createdCupcakeData);
  addCupcakesToList([createdCupcakeData]);
}

$form.on('submit', handleSubmit);
console.log('Added submit event listener');

/**
 * Get all cupcake data from API
 *
 */

async function getCupcakesData(){
  const response = await fetch(`${BASE_URL}/api/cupcakes`);
  const cupcakesData = (await response.json()).cupcakes;

  console.log("cupcakes data is:", cupcakesData);
  // const cupcakes = cupcakesData.map(cupcake => {flavor, image_url, rating, size})

  // console.log("cupcakes is:", cupcakes);

  return cupcakesData
}


// have getting a list of cupcakes - we want to list them
// create a ul
// create a for loop, and create html elements and append


function addCupcakesToList(cupcakes){
  const $list = $('<ul>');

  for(const cupcake of cupcakes){
    const $cupcakeListItem = $(`<li> Flavor: ${cupcake.flavor},
    Rating: ${cupcake.rating}, Size: ${cupcake.size} </li>
    <img src=${cupcake.image_url} class="img-thumbnail">`);

    $list.append($cupcakeListItem);
  }

  $results.append($list);
}


async function start(){
  const cupcakeData = await getCupcakesData();
  addCupcakesToList(cupcakeData);
}

start();
// /**A render method to render HTML for an individual cupcake */
// function generateCupcakeMarkup(cupcakes){
//   retur
// }

