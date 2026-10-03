document.addEventListener('DOMContentLoaded', () => {
  let currentExam = null;
  let currentSessionId = null;
  let currentQIndex = 0;
  let userAnswers = {}; // { qid: selectedIndex }
  let timerInterval = null;
  let secondsRemaining = 0;
  let startTime = 0;

  const launcherContainer = document.getElementById('exams-list-container');
  const launcherView = document.getElementById('exam-launcher-view');
  const activeExamView = document.getElementById('active-exam-view');
  const resultsView = document.getElementById('exam-results-view');

  const timerDisplay = document.getElementById('timer-display');
  const timerBox = document.getElementById('timer-box');
  const activeExamTitle = document.getElementById('active-exam-title');
  const activeExamMeta = document.getElementById('active-exam-meta');

  const examQTopic = document.getElementById('exam-q-topic');
  const examQCounter = document.getElementById('exam-q-counter');
  const examQText = document.getElementById('exam-q-text');
  const examOptionsContainer = document.getElementById('exam-options-container');
  const paletteContainer = document.getElementById('question-palette');
  const hintSection = document.getElementById('exam-hint-section');
  const hintDrawer = document.getElementById('exam-hint-drawer');

  let allExamsList = [];
  let currentCategoryFilter = 'all';

  const categoryTabs = document.getElementById('exam-category-tabs');
  if (categoryTabs) {
    categoryTabs.addEventListener('click', (e) => {
      const pill = e.target.closest('.topic-pill');
      if (!pill) return;
      document.querySelectorAll('#exam-category-tabs .topic-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentCategoryFilter = pill.dataset.category || 'all';
      filterAndRenderExams();
    });
  }

  // Load list of available mock exams
  async function loadExamsList() {
    try {
      const res = await fetch('/api/exams');
      const data = await res.json();
      if (data.ok && data.exams && data.exams.length > 0) {
        allExamsList = data.exams;
        filterAndRenderExams();
      } else {
        launcherContainer.innerHTML = `
          <div class="card" style="grid-column: span 3; text-align: center; padding: 40px;">
            <div style="font-size: 32px; margin-bottom: 12px;">📝</div>
            <h3 style="font-size: 18px; font-weight: 700; margin-bottom: 8px;">No Mock Exams Available</h3>
            <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 20px;">Generate or re-seed placement mock exams.</p>
            <button class="btn btn-secondary" onclick="seedDefaultExam()">Generate Placement Mocks ⚡</button>
          </div>
        `;
      }
    } catch (err) {
      console.error('Error fetching exams:', err);
      launcherContainer.innerHTML = `<p class="page-subtitle">Failed to load mock exams list.</p>`;
    }
  }

  function filterAndRenderExams() {
    let filtered = allExamsList;
    if (currentCategoryFilter !== 'all') {
      filtered = allExamsList.filter(ex => {
        const cat = (ex.category || ex.topic || '').toLowerCase();
        return cat.includes(currentCategoryFilter.toLowerCase());
      });
    }
    renderExamsList(filtered.length ? filtered : allExamsList);
  }

  function renderExamsList(exams) {
    launcherContainer.innerHTML = '';
    exams.forEach(ex => {
      const card = document.createElement('div');
      card.className = 'card hover-lift';
      card.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
          <span class="badge badge-medium">${ex.category || ex.topic || 'General Aptitude'}</span>
          <span style="font-size: 12px; color: var(--accent-cyan); font-weight: 700;">⏱️ 20 Mins • 20 Questions</span>
        </div>
        <h3 style="font-size: 18px; font-weight: 700; color: var(--text-main); margin-bottom: 8px;">${ex.name}</h3>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 18px;">
          Timed placement assessment simulating industry campus recruitment test conditions.
        </p>
        <button class="btn" style="width: 100%;" onclick="promptExamDifficulty('${ex._id}')">Start Test ➔</button>
      `;
      launcherContainer.appendChild(card);
    });
  }

  let pendingExamId = null;
  let selectedDifficulty = 'mixed';

  window.promptExamDifficulty = function(examId) {
    pendingExamId = examId;
    selectedDifficulty = 'mixed';
    document.querySelectorAll('.diff-card').forEach(c => {
      c.classList.toggle('selected', c.getAttribute('data-diff') === 'mixed');
    });
    const modal = document.getElementById('difficulty-modal');
    if (modal) modal.style.display = 'flex';
  };

  window.closeDifficultyModal = function() {
    const modal = document.getElementById('difficulty-modal');
    if (modal) modal.style.display = 'none';
    pendingExamId = null;
  };

  window.selectDifficulty = function(diff) {
    selectedDifficulty = diff;
    document.querySelectorAll('.diff-card').forEach(c => {
      c.classList.toggle('selected', c.getAttribute('data-diff') === diff);
    });
  };

  window.confirmLaunchExam = function() {
    if (!pendingExamId) return;
    const targetExamId = pendingExamId;
    const diff = selectedDifficulty;
    closeDifficultyModal();
    startExamSession(targetExamId, diff);
  };

  window.seedDefaultExam = async function() {
    try {
      const res = await fetch('/api/create-demo-exam', {method: 'POST'});
      const data = await res.json();
      if (data.ok) {
        loadExamsList();
      } else {
        alert(data.error || 'Failed to create demo exam');
      }
    } catch (e) {
      alert('Error creating demo exam');
    }
  };

  window.startExamSession = async function(examId, difficulty = 'mixed') {
    try {
      // Start session with chosen difficulty mode
      const sessRes = await fetch('/api/start-exam', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({exam_id: examId, difficulty: difficulty})
      });
      const sessData = await sessRes.json();
      if (!sessData.ok) {
        alert(sessData.error || 'Could not start exam session');
        return;
      }
      currentSessionId = sessData.session_id;
      currentExam = sessData.exam;

      // If exam details weren't directly returned, fetch with session_id
      if (!currentExam || !currentExam.questions || currentExam.questions.length === 0) {
        const examRes = await fetch(`/api/get-exam/${examId}?session_id=${currentSessionId}`);
        const examData = await examRes.json();
        if (!examData.ok || !examData.exam) {
          alert('Could not load exam details');
          return;
        }
        currentExam = examData.exam;
      }

      // Reset exam state - Standard 20 Minutes (1,200 seconds)
      currentQIndex = 0;
      userAnswers = {};
      currentExam.duration_minutes = 20;
      secondsRemaining = 20 * 60; // 20 minutes countdown
      startTime = Date.now();

      // Show Active View
      launcherView.style.display = 'none';
      resultsView.style.display = 'none';
      activeExamView.style.display = 'block';

      activeExamTitle.textContent = currentExam.name;
      activeExamMeta.textContent = `Timed Assessment (20 Minutes • 20 Questions) • Mode: ${(difficulty || 'mixed').toUpperCase()}`;

      if (hintSection) {
        hintSection.style.display = 'block';
      }

      startTimer();
      renderPalette();
      renderExamQuestion();
    } catch (err) {
      console.error('Error launching exam session:', err);
      alert('Failed to launch exam. Please try again.');
    }
  };

  function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    updateTimerDisplay();

    timerInterval = setInterval(() => {
      secondsRemaining--;
      updateTimerDisplay();

      if (secondsRemaining <= 0) {
        clearInterval(timerInterval);
        alert('Time is up! Submitting your exam automatically.');
        submitExam();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(secondsRemaining / 60);
    const secs = secondsRemaining % 60;
    timerDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    if (secondsRemaining < 300) {
      timerBox.classList.add('warning');
    } else {
      timerBox.classList.remove('warning');
    }
  }

  function renderPalette() {
    paletteContainer.innerHTML = '';
    currentExam.questions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      if (idx === currentQIndex) btn.classList.add('active');
      if (userAnswers[q._id] !== undefined) btn.classList.add('answered');
      btn.textContent = idx + 1;
      btn.onclick = () => {
        currentQIndex = idx;
        renderExamQuestion();
      };
      paletteContainer.appendChild(btn);
    });
  }

  function renderExamQuestion() {
    if (!currentExam || !currentExam.questions[currentQIndex]) return;

    const q = currentExam.questions[currentQIndex];
    examQTopic.textContent = q.topic || q.category || 'General';
    examQCounter.textContent = `Question ${currentQIndex + 1} of ${currentExam.questions.length}`;
    examQText.textContent = q.question;

    // Display question difficulty badge
    const diffEl = document.getElementById('exam-q-diff');
    if (diffEl) {
      const d = (q.difficulty || 'medium').toLowerCase();
      diffEl.textContent = d.toUpperCase();
      diffEl.className = 'badge ' + (d === 'easy' ? 'badge-easy' : (d === 'hard' ? 'badge-hard' : 'badge-medium'));
    }

    const drawer = document.getElementById('exam-hint-drawer');
    if (drawer) drawer.style.display = 'none';

    // Render options
    examOptionsContainer.innerHTML = '';
    const prefixes = ['A', 'B', 'C', 'D', 'E'];
    const currentSelected = userAnswers[q._id];

    (q.options || []).forEach((optText, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn' + (currentSelected === idx ? ' selected' : '');
      btn.innerHTML = `<span class="option-prefix">${prefixes[idx] || (idx+1)}</span><span>${optText}</span>`;
      btn.onclick = () => {
        userAnswers[q._id] = idx;
        renderExamQuestion();
        renderPalette();
      };
      examOptionsContainer.appendChild(btn);
    });

    document.getElementById('exam-btn-prev').disabled = currentQIndex === 0;
    document.getElementById('exam-btn-next').disabled = currentQIndex === currentExam.questions.length - 1;
  }

  window.examPrevQ = function() {
    if (currentQIndex > 0) {
      currentQIndex--;
      renderExamQuestion();
      renderPalette();
    }
  };

  window.examNextQ = function() {
    if (currentQIndex < currentExam.questions.length - 1) {
      currentQIndex++;
      renderExamQuestion();
      renderPalette();
    }
  };

  window.clearExamChoice = function() {
    const q = currentExam.questions[currentQIndex];
    if (q && userAnswers[q._id] !== undefined) {
      delete userAnswers[q._id];
      renderExamQuestion();
      renderPalette();
    }
  };

  window.fetchExamHint = async function(level = 1) {
    const q = currentExam.questions[currentQIndex];
    if (!q) return;
    const drawer = document.getElementById('exam-hint-drawer');
    const content = document.getElementById('exam-hint-content');
    const title = document.getElementById('exam-hint-level-title');

    if (!drawer || !content) return;
    drawer.style.display = 'block';

    const levelTitles = {
      1: '💡 Level 1 – Basic Hint',
      2: '🔍 Level 2 – Detailed Hint',
      3: '🎓 Level 3 – Solution'
    };
    if (title) title.textContent = levelTitles[level] || `Hint (Level ${level})`;
    content.textContent = 'Generating progressive hint...';

    try {
      const res = await fetch('/api/get-hint', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question_id: q._id, level: level})
      });
      const data = await res.json();
      if (data.ok) {
        content.textContent = data.hint;
      } else {
        content.textContent = data.error || 'Hint unavailable.';
      }
    } catch (e) {
      content.textContent = 'Error fetching hint.';
    }
  };

  window.confirmSubmitExam = function() {
    const total = currentExam.questions.length;
    const answeredCount = Object.keys(userAnswers).length;
    const msg = `You have answered ${answeredCount} out of ${total} questions. Submit test now?`;
    if (confirm(msg)) {
      submitExam();
    }
  };

  async function submitExam() {
    if (timerInterval) clearInterval(timerInterval);
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);

    try {
      const res = await fetch('/api/submit-exam', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          session_id: currentSessionId,
          answers: userAnswers,
          time_taken_seconds: timeSpent
        })
      });
      const data = await res.json();
      if (data.ok && data.result) {
        renderResults(data.result);
      } else {
        alert(data.error || 'Failed to score exam.');
      }
    } catch (err) {
      console.error(err);
      alert('Network error submitting exam.');
    }
  }

  function renderResults(res) {
    activeExamView.style.display = 'none';
    resultsView.style.display = 'block';

    const score = res.score || 0;
    document.getElementById('result-score-val').textContent = `${score}%`;
    document.getElementById('result-correct-cnt').textContent = `${res.correct_count} / ${res.total_questions}`;
    
    // Time formatting
    const secs = res.time_taken_seconds || 0;
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    document.getElementById('result-time-taken').textContent = `${m}m ${s}s`;

    // Rating emoji
    if (score >= 80) {
      document.getElementById('result-emoji').textContent = '🏆';
      document.getElementById('result-rating').textContent = 'EXCELLENT';
    } else if (score >= 60) {
      document.getElementById('result-emoji').textContent = '🎯';
      document.getElementById('result-rating').textContent = 'GOOD';
    } else {
      document.getElementById('result-emoji').textContent = '📚';
      document.getElementById('result-rating').textContent = 'NEEDS PRACTICE';
    }

    // Detailed Breakdown List
    const list = document.getElementById('breakdown-list');
    list.innerHTML = '';
    const prefixes = ['A', 'B', 'C', 'D', 'E'];

    (res.details || []).forEach((item, idx) => {
      const isCorrect = item.is_correct;
      const card = document.createElement('div');
      card.className = 'card';
      card.style.background = isCorrect ? 'rgba(16, 185, 129, 0.05)' : 'rgba(244, 63, 94, 0.05)';
      card.style.borderColor = isCorrect ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)';

      const userSelStr = item.selected !== null && item.selected !== undefined ? `Choice ${prefixes[item.selected]}` : 'Not Answered';
      const correctSelStr = `Choice ${prefixes[item.correct_index]}`;

      card.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-size: 13px; font-weight: 700; color: var(--text-muted);">Question ${idx + 1} (${item.topic || 'General'})</span>
          <span class="badge ${isCorrect ? 'badge-easy' : 'badge-hard'}">${isCorrect ? '✓ CORRECT' : '✕ INCORRECT'}</span>
        </div>
        <h4 style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">${item.question_text || 'Question'}</h4>
        <div style="font-size: 13px; display: flex; gap: 16px; margin-bottom: 8px;">
          <span>Your Answer: <strong style="color: ${isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">${userSelStr}</strong></span>
          <span>Correct Answer: <strong style="color: var(--accent-emerald);">${correctSelStr}</strong></span>
        </div>
        ${item.explanation ? `<div style="font-size: 12px; color: var(--text-muted); margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.05);">💡 Explanation: ${item.explanation}</div>` : ''}
      `;
      list.appendChild(card);
    });
  }

  window.resetToExamsList = function() {
    resultsView.style.display = 'none';
    activeExamView.style.display = 'none';
    launcherView.style.display = 'block';
    loadExamsList();
  };

  // Initial load
  loadExamsList();
});
