"use strict";

const BASE_URL = "http://localhost:5000";

const $FORM = $('#create-cupcake');
const $RESULTS = $('#cupcake-results');

/**
 * find form,
 * set event listener for create cupcake
 * fetch request to flask api
 * show response on page
 */

/**
 * Get inputs from form and submit post request to create cupcake
 *
 * No inputs, use user input values from form
 * Return object with data for the added cupcake
 */

async function getCreateCupcakeResult() {
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

/**
 * Show added cupcake on cupcake list
 */


/** Conductor function to recieve form submit and show results */

async function handleSubmit(evt) {
  evt.preventDefault();
  console.log('event for form submit:', evt)

  const createdCupcakeData = await getCreateCupcakeResult();
  console.log('create cupcake result:', createdCupcakeData);

}

$FORM.on('submit', handleSubmit);
console.log('Added submit event listener');