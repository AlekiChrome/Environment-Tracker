import { streamGemini } from './generator.js';

const form = document.querySelector('form');
const promptInput = document.querySelector('input[name="insert-prompt"]');
const output = document.querySelector('.output');

form.onsubmit = async (ev) => {
  ev.preventDefault();
  output.textContent = 'Generating...';

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
  } catch (e) {
    output.innerHTML += '<hr>' + e;
  }
};