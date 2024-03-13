"use strict";

console.log('safdasf');
const $likeButton = $("#like-button");
const $unlikeButton = $("#unlike-button");

async function addLike(evt) {
  evt.preventDefault();

  const response = await fetch(`/api/like`, {
    method: "POST",
    body: JSON.stringify({
      cafe_id: 1,
    }),
    headers: {
      "content-type": "application/json",
    }
  })

  const result = await response.json();
  console.log(result);
  if (result.liked) {
    $likeButton.hide();
    $unlikeButton.show();
  }
}



async function removeLike(evt) {
  evt.preventDefault();

  const response = await fetch(`/api/unlike`, {
    method: "POST",
    body: JSON.stringify({
      cafe_id: 1,
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

$unlikeButton.on("submit", unlike);
$likeButton.on("submit", like);