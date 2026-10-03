// AptiForge - LeetCode-Grade Practice Portal Controller
document.addEventListener('DOMContentLoaded', () => {
  let questionsList = [];
  let currentIndex = 0;
  let currentTopic = 'all';
  let currentDifficulty = 'mixed';
  let isAnswered = false;
  let hintCache = {}; // Cache hints per qid: { 1: hint1, 2: hint2, 3: hint3 }

  // DOM Elements
  const topicContainer = document.getElementById('topic-container');
  const questionTopicEl = document.getElementById('question-topic');
  const questionDiffEl = document.getElementById('question-difficulty');
  const questionCounterEl = document.getElementById('question-counter');
  const questionTitleHeading = document.getElementById('question-title-heading');
  const questionTextEl = document.getElementById('question-text');
  const optionsContainer = document.getElementById('options-container');
  const currentQidInput = document.getElementById('current-qid');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const lcConsole = document.getElementById('lc-console');
  const lcVerdict = document.getElementById('lc-verdict');
  const lcMetaFeedback = document.getElementById('lc-meta-feedback');
  const lcExplanationText = document.getElementById('lc-explanation-text');
  const timerDisplayEl = document.getElementById('practice-timer-display');

  // Handle URL query params (e.g. ?topic=Quantitative)
  const urlParams = new URLSearchParams(window.location.search);
  const initialTopic = urlParams.get('topic');
  if (initialTopic) {
    currentTopic = initialTopic;
    const pill = document.querySelector(`.topic-pill[data-topic="${initialTopic}"]`);
    if (pill) {
      document.querySelectorAll('#topic-container .topic-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    }
  }

  // Topic pill clicks
  if (topicContainer) {
    topicContainer.addEventListener('click', (e) => {
      const pill = e.target.closest('.topic-pill');
      if (!pill || !pill.dataset.topic) return;
      document.querySelectorAll('#topic-container .topic-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentTopic = pill.dataset.topic;
      fetchQuestions();
    });
  }

  // Change difficulty
  window.changePracticeDifficulty = function(diff) {
    currentDifficulty = diff;
    document.querySelectorAll('#practice-difficulty-tabs .topic-pill').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-diff') === diff);
    });
    fetchQuestions();
  };

  // 20-minute practice timer
  let practiceSecondsRemaining = 20 * 60;
  let practiceTimerInterval = null;

  function startPracticeTimer() {
    if (practiceTimerInterval) clearInterval(practiceTimerInterval);
    practiceSecondsRemaining = 20 * 60;
    updatePracticeTimerDisplay();

    practiceTimerInterval = setInterval(() => {
      practiceSecondsRemaining--;
      updatePracticeTimerDisplay();
      if (practiceSecondsRemaining <= 0) {
        clearInterval(practiceTimerInterval);
        if (timerDisplayEl) timerDisplayEl.textContent = '⏱️ 00:00 (Time Up)';
        alert('20-minute practice session time is up! Great effort.');
      }
    }, 1000);
  }

  function updatePracticeTimerDisplay() {
    if (!timerDisplayEl) return;
    const m = Math.floor(practiceSecondsRemaining / 60);
    const s = practiceSecondsRemaining % 60;
    timerDisplayEl.textContent = `⏱️ ${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  window.reloadRandom20Questions = function() {
    fetchQuestions();
  };

  async function fetchQuestions() {
    questionTextEl.textContent = 'Selecting 20 high-yield questions...';
    optionsContainer.innerHTML = '';
    if (lcConsole) lcConsole.style.display = 'none';
    resetAccordions();

    try {
      const res = await fetch(`/api/questions?topic=${encodeURIComponent(currentTopic)}&difficulty=${encodeURIComponent(currentDifficulty)}&random=true&limit=20`);
      const data = await res.json();
      if (data.ok && data.questions && data.questions.length > 0) {
        questionsList = data.questions;
        currentIndex = 0;
        hintCache = {};
        startPracticeTimer();
        renderQuestion();
      } else {
        questionTextEl.textContent = 'No questions found for this topic or difficulty. Please select another category.';
        questionCounterEl.textContent = 'Problem 0 of 0';
        optionsContainer.innerHTML = '';
        btnPrev.disabled = true;
        btnNext.disabled = true;
      }
    } catch (err) {
      console.error('Error fetching questions:', err);
      questionTextEl.textContent = 'Failed to load questions. Please check connection.';
    }
  }

  function resetAccordions() {
    for (let i = 1; i <= 3; i++) {
      const acc = document.getElementById(`acc-hint-${i}`);
      const body = document.getElementById(`acc-body-${i}`);
      if (acc) acc.classList.remove('open');
      if (body) {
        body.innerHTML = '<em>Loading pedagogical hint...</em>';
      }
    }
  }

  function renderQuestion() {
    if (!questionsList.length || currentIndex < 0 || currentIndex >= questionsList.length) return;

    const q = questionsList[currentIndex];
    isAnswered = false;
    currentQidInput.value = q._id;

    // Heading and tags
    questionTitleHeading.textContent = `Problem #${currentIndex + 1}: ${q.topic || 'Aptitude Challenge'}`;
    questionTopicEl.textContent = q.topic || 'General';

    const diff = (q.difficulty || 'medium').toLowerCase();
    questionDiffEl.textContent = diff.toUpperCase();
    questionDiffEl.className = diff === 'easy' ? 'lc-tag-easy' : (diff === 'hard' ? 'lc-tag-hard' : 'lc-tag-medium');

    questionCounterEl.textContent = `Problem ${currentIndex + 1} of ${questionsList.length}`;
    questionTextEl.textContent = q.question;

    // Reset console & accordions
    if (lcConsole) lcConsole.style.display = 'none';
    resetAccordions();

    // Render multiple-choice options with LeetCode cards
    optionsContainer.innerHTML = '';
    const prefixes = ['A', 'B', 'C', 'D', 'E'];

    (q.options || []).forEach((optText, idx) => {
      const card = document.createElement('div');
      card.className = 'lc-option-card';
      card.dataset.index = idx;
      card.innerHTML = `
        <div class="lc-option-key">${prefixes[idx] || (idx + 1)}</div>
        <div style="flex: 1; line-height: 1.4;">${optText}</div>
      `;
      card.addEventListener('click', () => handleOptionSelect(idx, card));
      optionsContainer.appendChild(card);
    });

    btnPrev.disabled = currentIndex === 0;
    btnNext.disabled = currentIndex === questionsList.length - 1;
  }

  async function handleOptionSelect(selectedIndex, selectedCard) {
    if (isAnswered) return;
    isAnswered = true;

    const qid = currentQidInput.value;
    const cards = optionsContainer.querySelectorAll('.lc-option-card');
    cards.forEach(c => c.style.pointerEvents = 'none');

    selectedCard.classList.add('selected');

    try {
      const startTime = performance.now();
      const res = await fetch('/api/verify-answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question_id: qid, selected_index: selectedIndex})
      });
      const data = await res.json();
      const timeElapsed = Math.round(performance.now() - startTime);

      if (data.ok) {
        selectedCard.classList.remove('selected');
        if (data.is_correct) {
          selectedCard.classList.add('correct');
          lcVerdict.className = 'lc-verdict-banner lc-verdict-accepted';
          lcVerdict.innerHTML = '<span>✓</span> Accepted';
          lcMetaFeedback.textContent = `Response Time: ${timeElapsed}ms | Correct Answer`;
        } else {
          selectedCard.classList.add('wrong');
          lcVerdict.className = 'lc-verdict-banner lc-verdict-wrong';
          lcVerdict.innerHTML = '<span>✗</span> Wrong Answer';
          lcMetaFeedback.textContent = `Response Time: ${timeElapsed}ms | Incorrect choice`;

          // Highlight the actual correct option
          const correctCard = optionsContainer.querySelector(`.lc-option-card[data-index="${data.correct_index}"]`);
          if (correctCard) correctCard.classList.add('correct');
        }

        // Display explanation in LeetCode console
        if (data.explanation) {
          lcExplanationText.textContent = data.explanation;
          lcConsole.style.display = 'block';
        }

        // Also pre-cache solution hint level 3
        if (data.explanation) {
          if (!hintCache[qid]) hintCache[qid] = {};
          hintCache[qid][3] = data.explanation;
        }
      } else {
        alert(data.error || 'Verification failed');
      }
    } catch (err) {
      console.error(err);
      alert('Network error verifying answer.');
    } finally {
      cards.forEach(c => c.style.pointerEvents = 'auto');
    }
  }

  // Accordion toggle & dynamic progressive hint fetching
  window.toggleAccordion = async function(accId, level) {
    const acc = document.getElementById(accId);
    const body = document.getElementById(`acc-body-${level}`);
    if (!acc || !body) return;

    const isOpen = acc.classList.contains('open');

    if (isOpen) {
      acc.classList.remove('open');
      return;
    }

    acc.classList.add('open');

    const qid = currentQidInput.value;
    if (!qid) return;

    if (hintCache[qid] && hintCache[qid][level]) {
      body.textContent = hintCache[qid][level];
      return;
    }

    body.innerHTML = '<em>⚡ Analyzing mathematical structure & compiling pedagogical hint...</em>';

    try {
      const res = await fetch('/api/get-hint', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question_id: qid, level: level})
      });
      const data = await res.json();
      if (data.ok && data.hint) {
        if (!hintCache[qid]) hintCache[qid] = {};
        hintCache[qid][level] = data.hint;
        body.textContent = data.hint;
      } else {
        body.textContent = data.error || 'Hint could not be retrieved.';
      }
    } catch (err) {
      console.error('Error fetching hint:', err);
      body.textContent = 'Error connecting to hint service.';
    }
  };

  // Tab switching inside left problem panel
  window.switchLeftTab = function(tabName) {
    document.querySelectorAll('.lc-panel-tab').forEach(t => t.classList.remove('active'));
    const clickedTab = document.getElementById(`tab-${tabName}`);
    if (clickedTab) clickedTab.classList.add('active');

    if (tabName === 'desc') {
      // scroll to problem content
      questionTextEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else if (tabName === 'hints') {
      const acc1 = document.getElementById('acc-hint-1');
      if (acc1 && !acc1.classList.contains('open')) {
        toggleAccordion('acc-hint-1', 1);
      }
      acc1.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else if (tabName === 'solution') {
      const acc3 = document.getElementById('acc-hint-3');
      if (acc3 && !acc3.classList.contains('open')) {
        toggleAccordion('acc-hint-3', 3);
      }
      acc3.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  window.prevQuestion = function() {
    if (currentIndex > 0) {
      currentIndex--;
      renderQuestion();
    }
  };

  window.nextQuestion = function() {
    if (currentIndex < questionsList.length - 1) {
      currentIndex++;
      renderQuestion();
    }
  };

  window.randomQuestion = function() {
    if (questionsList.length > 1) {
      let rand = Math.floor(Math.random() * questionsList.length);
      if (rand === currentIndex) rand = (rand + 1) % questionsList.length;
      currentIndex = rand;
      renderQuestion();
    }
  };

  // Initialize
  fetchQuestions();
});
