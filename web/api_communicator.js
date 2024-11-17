import { streamGemini } from './generator.js';

const form = document.querySelector('form');
const promptInput = document.querySelector('input[name="insert-prompt"]');
const output = document.querySelector('.output');
const searchesList = document.getElementById('searches-list');
const clearHistoryButton = document.getElementById('clear-history');

const loadPreviousSearches = async () => {
  try {
      const response = await fetch("/api/searches");
      const searches = await response.json();

      searchesList.innerHTML = "";

  searches.forEach(search => {
      if (search) { 
        const li = document.createElement("li");
        li.textContent = search;
        searchesList.appendChild(li);
      }
    });
  } catch (error) {
    console.error("Error loading previous searches:", error);
  }
};

form.onsubmit = async (ev) => {
  ev.preventDefault();
  output.textContent = "Generating...";

  try {
    let contents = [
      {
        type: "text",
        text: promptInput.value,
      }
    ];

    let stream = streamGemini({
      model: 'gemini-1.5-flash',
      contents,
    });

    let buffer = [];
    let md = new markdownit();
    for await (let chunk of stream) {
      buffer.push(chunk);
      output.innerHTML = md.render(buffer.join(''));
    }

    // await saveSearch(promptInput.value);
    loadPreviousSearches();
  } catch (error) {
    output.innerHTML += "<hr>Error: " + error.message;
    console.error("Error during generation:", error);
  }
};

clearHistoryButton.addEventListener("click", async () => {
  try {
    const response = await fetch("/api/clear_searches", { method: "POST" });
    const result = await response.json();

    if (result.success) {
      searchesList.innerHTML = "";
      alert("Search history cleared.");
    } else {
      alert("Error clearing history.");
    }
  } catch (error) {
    console.error("Error clearing history:", error);
  }
});

window.addEventListener("DOMContentLoaded", loadPreviousSearches);

