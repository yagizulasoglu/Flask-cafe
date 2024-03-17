"use strict";

const $likeButton = $("#like-button");
const $unlikeButton = $("#unlike-button");
const $likeForm = $("#like-form");
const $unlikeForm = ($("#unlike-form"));
const cafeId = $('#unlike-button').data('id');

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
    $(`#cafe-${cafeId}`).remove();
  }
}
$(document).ready(displayButton);
$unlikeForm.on("submit", removeLike);
$likeForm.on("submit", addLike);