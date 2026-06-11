const params = new URLSearchParams(window.location.search);
const ADVENTURE_ID = params.get("adventure");
const START_SCENE = "start";

if (!ADVENTURE_ID) {
  alert("No adventure specified.");
}

let historyStack = [];
let currentScene = null;

const sceneText = document.getElementById("scene-text");
const sceneImage = document.getElementById("scene-image");
const choicesDiv = document.getElementById("choices");
const backButton = document.getElementById("back-button");

async function loadScene(sceneId, pushHistory = true) {
  if (currentScene && pushHistory) {
    historyStack.push(currentScene);
  }

  const response = await fetch(
    `/adventure/${ADVENTURE_ID}/scene/${sceneId}`
  );
  const scene = await response.json();

  renderScene(scene);
  currentScene = sceneId;
  updateBackButton();
}

function renderScene(scene) {
  sceneText.textContent = scene.text;

  if (scene.image) {
    console.log("attempting to load image:", scene.image)
    sceneImage.src = scene.image;
    sceneImage.hidden = false;
  } else {
    sceneImage.hidden = true;
  }

  choicesDiv.innerHTML = "";

  scene.choices.forEach(choice => {
    const btn = document.createElement("button");
    btn.textContent = choice.label;
    btn.onclick = () => loadScene(choice.next);
    choicesDiv.appendChild(btn);
  });
}

function goBack() {
  if (historyStack.length === 0) return;
  const previous = historyStack.pop();
  loadScene(previous, false);
}

function updateBackButton() {
  backButton.disabled = historyStack.length === 0;
}

backButton.onclick = goBack;

loadScene(START_SCENE, false);
