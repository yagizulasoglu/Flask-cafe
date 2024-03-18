"use strict";

const $likeButton = $("#like-button");
const $unlikeButton = $("#unlike-button");
const $likeForm = $("#like-form");
const $unlikeForm = ($("#unlike-form"));
const cafeId = $('#unlike-button').data('id');

/**The function is for the initial page. If the user liked the cafe before,
 * it only shows the unlike button. It shows the like button otherwise.
 */
async function displayButton() {
  let response = await fetch(`/api/likes?cafe_id=${cafeId}`, {
    method: "GET",
    headers: {
      "content-type": "application/json",
    }
  })

  const result = await response.json();
  if (result.likes) {
    $likeButton.hide();
    $unlikeButton.show();
  } else {
    $unlikeButton.hide();
    $likeButton.show();
  }
}


/**When the user likes a cafe, It sends a post request and shows the unlike
 * button instead of the like button.
 */

async function addLike(evt) {
  evt.preventDefault();
  const response = await fetch("/api/like", {
    method: "POST",
    body: JSON.stringify({
      cafe_id: cafeId,
    }),
    headers: {
      "content-type": "application/json",
    }
  })

  const result = await response.json();

  if (result.liked) {
    $likeButton.hide();
    $unlikeButton.show();
  }
}

/**When the user unlikes a cafe, It sends a post request and shows the like
 * button instead of the unlike button.
 */

async function removeLike(evt) {
  evt.preventDefault();

  const response = await fetch("/api/unlike", {
    method: "POST",
    body: JSON.stringify({
      cafe_id: cafeId,
    }),
    headers: {
      "content-type": "application/json",
    }
  })

  const result = await response.json();

  if (!result.liked) {
    $unlikeButton.hide();
    $likeButton.show();
  }
}
$(document).ready(displayButton);
$unlikeForm.on("submit", removeLike);
$likeForm.on("submit", addLike);