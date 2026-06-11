async function loadAdventures() {
  const response = await fetch("/api/adventures");
  const adventures = await response.json();

  const list = document.getElementById("adventure-list");
  list.innerHTML = "";

  adventures.forEach(adventure => {
    const btn = document.createElement("button");
    btn.textContent = adventure;
    btn.onclick = () => {
      window.location.href = `/play?adventure=${encodeURIComponent(adventure)}`;
    };
    list.appendChild(btn);
  });
}

loadAdventures();
