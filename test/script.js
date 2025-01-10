$(document).ready(function() {
  function simulateChat(userMessage) {
    const chatBox = $(".box");

    function addMessage(message, isUser) {
      const itemClass = isUser ? "right" : "";
      const msgClass = isUser ? "msg" : "msg";
      const icon = isUser ? "" : `<div class="icon"><i class="fa fa-user"></i></div>`;
      const messageHtml = `
        <div class="item ${itemClass}">
          ${icon}
          <div class="${msgClass}">
            <p>${message}</p>
          </div>
        </div>
        <br clear="both">
      `;
      chatBox.append(messageHtml);
      chatBox.scrollTop(chatBox[0].scrollHeight);
    }

    addMessage(userMessage, true);

    setTimeout(() => {
      const botMessage = "YES";
      addMessage(botMessage, false);
    }, 1000);
  }

  function handleUserInput() {
    const userInput = $("input[type='text']").val();
    if (userInput.trim() !== "") {
      simulateChat(userInput);
      $("input[type='text']").val("");
    }
  }

  $("button").on('click', handleUserInput);

  $("input[type='text']").on('keypress', function(e) {
    if (e.which === 13) {
      handleUserInput();
    }
  });
});
