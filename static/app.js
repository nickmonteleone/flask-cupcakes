"use strict";

const BASE_URL = "http://localhost:5000";

const $form = $('#create-cupcake');
const $results = $('#cupcake-results');


/** Get inputs from form and submit post request to create cupcake
 * Clear input values on form after cupcake creation.
 *
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

  // TODO: check solution for way to clear all field values from form
  for (let field of
    ['#flavor-input', '#size-input', '#rating-input', '#image_url-input']){
      $(field).val('');
    }

  return cupcakeData;
}

/** Conductor function to recieve form submit and create cupcake.
 * Append cupcake to cupcake list on page after creation.
 */

async function handleSubmit(evt) {
  evt.preventDefault();
  console.log('event for form submit:', evt);

  const createdCupcakeData = await getCreateCupcakeData();
  console.log('create cupcake result:', createdCupcakeData);
  addCupcakesToList([createdCupcakeData]);
}

/** Get all cupcake data from API.
 * Return list of cupcake data objects [{flavor, image_url, rating, size} ...]
 */

async function getCupcakesData() {
  const response = await fetch(`${BASE_URL}/api/cupcakes`);
  const responseJSON = await response.json();
  const cupcakesData = responseJSON.cupcakes;

  console.log("cupcakes data is:", cupcakesData);

  return cupcakesData;
}


/**A render method to create HTML for each cupcake in a list of cupcake data
 *
 * Input: list of cupcake objects.
 *  [{flavor, image_url, rating, size} ...]
 *
 * No return, add list objects to page.
*/

function addCupcakesToList(cupcakes) {
  const $list = $('<ul>');

  for (const cupcake of cupcakes) {
    const $cupcakeListItem = $(`<li> Flavor: ${cupcake.flavor},
    Rating: ${cupcake.rating}, Size: ${cupcake.size} </li>
    <img src=${cupcake.image_url} class="img-thumbnail w-25">`);

    $list.append($cupcakeListItem);
  }

  $results.append($list);
}

/** Start the app upon page opening. Get list of cupcakes from API
 * and add event listener to create cupcake form. */

async function start() {
  console.log('starting app');

  const cupcakeData = await getCupcakesData();
  addCupcakesToList(cupcakeData);

  $form.on('submit', handleSubmit);
}

start();
