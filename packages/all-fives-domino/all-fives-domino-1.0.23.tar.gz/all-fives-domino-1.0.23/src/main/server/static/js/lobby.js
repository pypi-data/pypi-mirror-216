let socket = io();

const lobby = new URLSearchParams(window.location.search).get("lobby");

socket.emit("join", lobby);