(function () {
  const form = document.getElementById('quizForm');
  const questions = document.querySelectorAll('.question-card');
  const timerDisplay = document.getElementById('timerDisplay');
  if (!form || !questions.length || !timerDisplay) return;

  const timePerQuestion = 30;
  let current = 0;
  let seconds = timePerQuestion;

  function showQuestion(index) {
    questions.forEach((q, i) => {
      q.style.display = i === index ? 'block' : 'none';
    });
  }

  function nextQuestion() {
    if (current < questions.length - 1) {
      current += 1;
      seconds = timePerQuestion;
      showQuestion(current);
    } else {
      form.submit();
    }
  }

  showQuestion(current);
  setInterval(() => {
    seconds -= 1;
    timerDisplay.textContent = String(Math.max(seconds, 0));
    if (seconds <= 0) {
      nextQuestion();
    }
  }, 1000);
})();
