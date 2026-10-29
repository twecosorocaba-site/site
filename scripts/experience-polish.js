/* TW&CO — campo de orientação com expansão apenas após o envio. */
(() => {
  'use strict';
  const form = document.getElementById('diagnosticForm');
  const field = document.getElementById('diagnosticText');
  const answer = document.getElementById('diagnosticAnswer');
  const message = document.getElementById('diagnosticReply');
  const link = document.getElementById('diagnosticWhatsApp');
  if (!form || !field || !answer || !message || !link) return;

  function setVisible(visible) {
    answer.classList.toggle('is-visible', visible);
    answer.setAttribute('aria-hidden', visible ? 'false' : 'true');
    answer.inert = !visible;
  }
  setVisible(false);

  // A orientação é gerada pelo script existente e continua encaminhando ao WhatsApp.
  // Este módulo controla apenas quando o resultado se torna visível.
  form.addEventListener('submit', () => {
    if (!field.validity.valid || field.value.trim().length < 8) return;
    if (!answer.classList.contains('is-visible')) {
      requestAnimationFrame(() => setVisible(true));
    } else {
      setVisible(true); // em novas perguntas, atualiza a resposta já aberta
    }
  });
})();
