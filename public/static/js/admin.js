// AptiForge - Admin Command Center Controller
document.addEventListener('DOMContentLoaded', () => {
  loadAdminQuestions();
  loadExamQuestionSelector();
  refreshAdminKPIs();

  // URL hash navigation support e.g. #upload, #roster
  if (window.location.hash) {
    const section = window.location.hash.replace('#', '');
    if (['questions', 'upload', 'exam', 'roster'].includes(section)) {
      showAdminSection(section);
    }
  }

  // Upload Form
  const uploadForm = document.getElementById('upload-form');
  if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById('file');
      if (!fileInput.files.length) {
        alert('Please choose a .PDF, .JSON, or .CSV file to upload.');
        return;
      }
      const fd = new FormData();
      fd.append('file', fileInput.files[0]);

      const topicInput = document.getElementById('upload-topic');
      if (topicInput) fd.append('topic', topicInput.value);

      const diffInput = document.getElementById('upload-difficulty');
      if (diffInput) fd.append('difficulty', diffInput.value);

      const btn = document.getElementById('upload-btn');
      btn.disabled = true;
      btn.textContent = 'Extracting & Ingesting Questions... ⏳';

      try {
        const res = await fetch('/api/upload-questions', {method: 'POST', body: fd});
        const data = await res.json();
        if (data.ok) {
          alert(`🎉 Success! Successfully extracted and ingested ${data.inserted || data.count || 0} questions into the live question bank.`);
          fileInput.value = '';
          const nameDisplay = document.getElementById('selected-file-name');
          if (nameDisplay) nameDisplay.textContent = '';
          loadAdminQuestions();
          refreshAdminKPIs();
          showAdminSection('questions');
        } else {
          alert('Upload failed: ' + (data.error || 'Server error'));
        }
      } catch (err) {
        console.error(err);
        alert('Network error uploading file. Please check server connection.');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Upload & Extract Questions ➔';
      }
    });
  }
});

window.refreshAdminKPIs = async function() {
  try {
    const res = await fetch('/api/admin/stats');
    const data = await res.json();
    if (data.ok && data.stats) {
      const s = data.stats;
      const elStudents = document.getElementById('kpi-students');
      const elQuestions = document.getElementById('kpi-questions');
      const elExams = document.getElementById('kpi-exams');
      const elAttempts = document.getElementById('kpi-attempts');

      if (elStudents) elStudents.textContent = s.total_students || 0;
      if (elQuestions) elQuestions.textContent = s.total_questions || 0;
      if (elExams) elExams.textContent = s.total_exams || 0;
      if (elAttempts) elAttempts.textContent = s.total_attempts || 0;
    }
  } catch (e) {
    console.warn('Could not refresh admin KPIs:', e);
  }
};

window.showAdminSection = function(secName) {
  ['questions', 'upload', 'exam', 'roster'].forEach(s => {
    const secEl = document.getElementById(`admin-sec-${s}`);
    const btnEl = document.getElementById(`tab-btn-${s}`);
    if (secEl) secEl.style.display = s === secName ? 'block' : 'none';
    if (btnEl) {
      if (s === secName) btnEl.classList.add('active');
      else btnEl.classList.remove('active');
    }
  });

  if (secName === 'questions') loadAdminQuestions();
  if (secName === 'exam') loadExamQuestionSelector();
  if (secName === 'roster') loadStudentRoster();
};

window.updateFileName = function(input) {
  const display = document.getElementById('selected-file-name');
  if (input.files && input.files.length) {
    display.textContent = `Selected File: ${input.files[0].name} (${(input.files[0].size/1024).toFixed(1)} KB)`;
  } else {
    display.textContent = '';
  }
};

let searchDebounceTimer = null;
window.debounceAdminSearch = function() {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    loadAdminQuestions();
  }, 300);
};

async function loadAdminQuestions() {
  const topic = document.getElementById('admin-topic-filter')?.value || 'all';
  const diff = document.getElementById('admin-diff-filter')?.value || 'all';
  const search = document.getElementById('admin-search-input')?.value || '';
  const tbody = document.getElementById('admin-questions-tbody');
  const countEl = document.getElementById('total-q-count');

  try {
    const url = `/api/questions?topic=${encodeURIComponent(topic)}&difficulty=${encodeURIComponent(diff)}&search=${encodeURIComponent(search)}&limit=300`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.ok && data.questions) {
      countEl.textContent = data.questions.length;
      if (data.questions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">No matching questions found. Try adjusting your search query or filters.</td></tr>`;
        return;
      }

      tbody.innerHTML = '';
      const prefixes = ['A', 'B', 'C', 'D', 'E'];

      data.questions.forEach(q => {
        const tr = document.createElement('tr');
        const correctStr = prefixes[q.answer_index] || 'A';
        const diffClass = q.difficulty === 'easy' ? 'lc-tag-easy' : (q.difficulty === 'hard' ? 'lc-tag-hard' : 'lc-tag-medium');

        tr.innerHTML = `
          <td style="font-weight: 500; max-width: 360px; line-height: 1.4;">
            <div style="font-weight: 600; color: #ffffff; margin-bottom: 4px;">${escapeHtml(q.question)}</div>
            <div style="font-size: 12px; color: #9ca3af;">${(q.options || []).length} Options Available</div>
          </td>
          <td><span class="lc-tag-topic">${q.topic || 'General'}</span></td>
          <td><span class="${diffClass}">${(q.difficulty || 'medium').toUpperCase()}</span></td>
          <td><strong style="color: #00b8a3; background: rgba(0,184,163,0.12); padding: 2px 8px; border-radius: 4px;">${correctStr}</strong></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-secondary btn-sm" onclick="inspectQuestion('${q._id}')" style="margin-right: 6px;">🔍 Inspect</button>
            <button class="btn btn-danger btn-sm" onclick="deleteQuestion('${q._id}')">🗑️ Delete</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error('Error loading questions:', err);
  }
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

window.deleteQuestion = async function(qid) {
  if (!confirm('Are you sure you want to permanently remove this question from the question bank?')) return;
  try {
    const res = await fetch(`/api/admin/questions/${qid}`, {method: 'DELETE'});
    const data = await res.json();
    if (data.ok) {
      loadAdminQuestions();
      refreshAdminKPIs();
    } else {
      alert(data.error || 'Failed to delete question.');
    }
  } catch (e) {
    alert('Error deleting question.');
  }
};

window.inspectQuestion = async function(qid) {
  const modal = document.getElementById('inspect-modal');
  const body = document.getElementById('inspect-modal-content');
  const title = document.getElementById('inspect-title');
  const diffBadge = document.getElementById('inspect-diff-badge');

  body.innerHTML = '<p style="color: #9ca3af; text-align: center; padding: 20px;">Fetching complete question architecture and hint steps...</p>';
  modal.style.display = 'flex';

  try {
    const res = await fetch(`/api/questions/${qid}`);
    const data = await res.json();
    if (data.ok && data.question) {
      const q = data.question;
      title.textContent = `Problem #${q._id.substring(q._id.length - 6).toUpperCase()} — ${q.topic || 'Aptitude'}`;
      
      const diff = (q.difficulty || 'medium').toLowerCase();
      diffBadge.textContent = diff.toUpperCase();
      diffBadge.className = diff === 'easy' ? 'lc-tag-easy' : (diff === 'hard' ? 'lc-tag-hard' : 'lc-tag-medium');

      const prefixes = ['A', 'B', 'C', 'D', 'E'];
      const optionsHtml = (q.options || []).map((opt, idx) => {
        const isCorrect = idx === q.answer_index;
        return `
          <div style="padding: 10px 14px; border-radius: 8px; margin-bottom: 6px; background: ${isCorrect ? 'rgba(0,184,163,0.12)' : '#262626'}; border: 1px solid ${isCorrect ? '#00b8a3' : '#333'}; display: flex; align-items: center; gap: 10px;">
            <span style="font-weight: 700; width: 24px; color: ${isCorrect ? '#00b8a3' : '#9ca3af'};">${prefixes[idx]}:</span>
            <span style="color: ${isCorrect ? '#00b8a3' : '#ffffff'}; font-weight: ${isCorrect ? '600' : '400'};">${escapeHtml(opt)}</span>
            ${isCorrect ? '<span style="margin-left: auto; font-size: 11px; font-weight: 700; color: #00b8a3;">✓ CORRECT ANSWER</span>' : ''}
          </div>
        `;
      }).join('');

      body.innerHTML = `
        <div style="margin-bottom: 20px;">
          <h4 style="font-size: 13px; font-weight: 700; color: #9ca3af; text-transform: uppercase; margin-bottom: 6px;">Problem Statement:</h4>
          <div style="font-size: 15px; color: #ffffff; line-height: 1.6; background: #242424; padding: 14px; border-radius: 8px; border: 1px solid #383838;">
            ${escapeHtml(q.question)}
          </div>
        </div>

        <div style="margin-bottom: 20px;">
          <h4 style="font-size: 13px; font-weight: 700; color: #9ca3af; text-transform: uppercase; margin-bottom: 6px;">Options & Answer:</h4>
          ${optionsHtml}
        </div>

        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="background: #181818; border: 1px solid #333333; border-radius: 8px; padding: 14px;">
            <div style="font-weight: 700; color: #38bdf8; font-size: 13px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
              <span>💡</span> Level 1 Hint (Core Theoretical Concept & Formula):
            </div>
            <div style="font-size: 13px; color: #d1d5db; line-height: 1.6; white-space: pre-line;">
              ${escapeHtml(q.hint_l1 || 'Not specified (Auto-generated concept on demand)')}
            </div>
          </div>

          <div style="background: #181818; border: 1px solid #333333; border-radius: 8px; padding: 14px;">
            <div style="font-weight: 700; color: #ffc01e; font-size: 13px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
              <span>🔍</span> Level 2 Hint (Equation Setup & Parameters):
            </div>
            <div style="font-size: 13px; color: #d1d5db; line-height: 1.6; white-space: pre-line;">
              ${escapeHtml(q.hint_l2 || 'Not specified (Auto-generated formulation on demand)')}
            </div>
          </div>

          <div style="background: #181818; border: 1px solid #333333; border-radius: 8px; padding: 14px; border-left: 4px solid #00b8a3;">
            <div style="font-weight: 700; color: #00b8a3; font-size: 13px; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
              <span>🎓</span> Level 3 Solution (Full Step-by-Step Textbook Derivation):
            </div>
            <div style="font-size: 13px; color: #d1d5db; line-height: 1.6; white-space: pre-line;">
              ${escapeHtml(q.explanation || 'No step-by-step derivation provided.')}
            </div>
          </div>
        </div>
      `;
    }
  } catch (err) {
    body.innerHTML = '<p style="color: #ff375f; text-align: center; padding: 20px;">Failed to load question details.</p>';
  }
};

window.closeInspectModal = function() {
  document.getElementById('inspect-modal').style.display = 'none';
};

window.openAddQuestionModal = function() {
  document.getElementById('question-modal').style.display = 'flex';
};

window.closeAddQuestionModal = function() {
  document.getElementById('question-modal').style.display = 'none';
};

window.handleSaveQuestion = async function(e) {
  e.preventDefault();
  const qText = document.getElementById('modal-q-text').value;
  const topic = document.getElementById('modal-q-topic').value;
  const difficulty = document.getElementById('modal-q-diff').value;
  const optA = document.getElementById('modal-opt-0').value;
  const optB = document.getElementById('modal-opt-1').value;
  const optC = document.getElementById('modal-opt-2').value;
  const optD = document.getElementById('modal-opt-3').value;
  const answerIndex = parseInt(document.getElementById('modal-correct-idx').value);
  const hint1 = document.getElementById('modal-hint-1').value;
  const hint2 = document.getElementById('modal-hint-2').value;
  const explanation = document.getElementById('modal-explanation').value;

  const payload = {
    questions: [{
      question: qText,
      topic: topic,
      difficulty: difficulty,
      options: [optA, optB, optC, optD],
      answer_index: answerIndex,
      hint_l1: hint1,
      hint_l2: hint2,
      explanation: explanation
    }]
  };

  try {
    const res = await fetch('/api/upload-questions', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.ok) {
      alert('Question added successfully!');
      closeAddQuestionModal();
      loadAdminQuestions();
      refreshAdminKPIs();
    } else {
      alert(data.error || 'Failed to save question.');
    }
  } catch (err) {
    alert('Error saving question.');
  }
};

async function loadExamQuestionSelector() {
  const container = document.getElementById('exam-questions-selector');
  try {
    const res = await fetch('/api/questions?topic=all&limit=250');
    const data = await res.json();
    if (data.ok && data.questions && data.questions.length > 0) {
      container.innerHTML = '';
      data.questions.forEach((q, idx) => {
        const div = document.createElement('div');
        div.style.cssText = 'display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04);';
        const checked = idx < 20 ? 'checked' : '';
        div.innerHTML = `
          <input type="checkbox" value="${q._id}" class="exam-q-chk" id="chk-${q._id}" ${checked} />
          <label for="chk-${q._id}" style="font-size: 13px; cursor: pointer; color: #d1d5db; line-height: 1.3;">
            <span style="color: #ffa116; font-weight: 600;">[${q.topic}]</span> 
            <span style="color: ${q.difficulty === 'easy' ? '#00b8a3' : (q.difficulty === 'hard' ? '#ff375f' : '#ffc01e')}; font-size: 11px; font-weight: 700;">(${q.difficulty.toUpperCase()})</span>
            ${escapeHtml(q.question)}
          </label>
        `;
        container.appendChild(div);
      });
    } else {
      container.innerHTML = `<p style="font-size: 13px; color: var(--text-muted);">No questions available. Please add questions first.</p>`;
    }
  } catch (e) {
    container.innerHTML = `<p style="font-size: 13px; color: var(--accent-rose);">Failed to load questions.</p>`;
  }
}

window.selectFirst20Questions = function() {
  const chks = document.querySelectorAll('.exam-q-chk');
  chks.forEach((c, idx) => {
    c.checked = idx < 20;
  });
};

window.selectAllQuestions = function(val) {
  const chks = document.querySelectorAll('.exam-q-chk');
  chks.forEach(c => c.checked = val);
};

window.handleCreateExam = async function(e) {
  e.preventDefault();
  const name = document.getElementById('exam-title').value;
  const duration = document.getElementById('exam-duration').value;
  const hints = document.getElementById('exam-hints-toggle').value === 'true';

  const chks = document.querySelectorAll('.exam-q-chk:checked');
  const qids = Array.from(chks).map(c => c.value);

  if (qids.length === 0) {
    alert('Please select at least 1 question for the mock test.');
    return;
  }

  try {
    const res = await fetch('/api/create-exam', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        name: name,
        duration_minutes: duration,
        enable_hints: hints,
        question_ids: qids
      })
    });
    const data = await res.json();
    if (data.ok) {
      alert(`Mock Exam "${name}" created successfully with ${qids.length} questions!`);
      refreshAdminKPIs();
      location.href = '/exam';
    } else {
      alert(data.error || 'Failed to create exam.');
    }
  } catch (err) {
    alert('Network error creating exam.');
  }
};

window.generateDemoExams = async function() {
  if (!confirm('This will seed the full set of 12 Company-Specific Placement Mock Tests. Proceed?')) return;
  try {
    const res = await fetch('/api/create-demo-exam', {method: 'POST'});
    const data = await res.json();
    if (data.ok) {
      alert(`Successfully generated 12 Placement Mock Exams!`);
      refreshAdminKPIs();
    }
  } catch (e) {
    alert('Failed to generate mock exams.');
  }
};

async function loadStudentRoster() {
  const tbody = document.getElementById('admin-roster-tbody');
  try {
    const res = await fetch('/api/admin/results');
    const data = await res.json();
    if (data.ok && data.results && data.results.length > 0) {
      tbody.innerHTML = '';
      data.results.forEach(r => {
        const tr = document.createElement('tr');
        const dateStr = r.created_at ? new Date(r.created_at).toLocaleDateString() : 'Recent';
        const isPass = r.score >= 70;

        tr.innerHTML = `
          <td style="font-weight: 600; color: #ffffff;">${escapeHtml(r.user_name || 'Student')}</td>
          <td style="color: #9ca3af; font-size: 13px;">${escapeHtml(r.user_email || 'student@domain.com')}</td>
          <td style="font-weight: 500;">${escapeHtml(r.exam_name || 'Mock Aptitude Test')}</td>
          <td>
            <span style="font-weight: 800; color: ${isPass ? '#00b8a3' : '#ff375f'}; background: ${isPass ? 'rgba(0,184,163,0.12)' : 'rgba(255,55,95,0.12)'}; padding: 3px 10px; border-radius: 12px; font-size: 13px;">
              ${r.score}%
            </span>
          </td>
          <td style="font-weight: 600; color: #e5e7eb;">${r.correct_count || 0} / ${r.total_questions || 0}</td>
          <td style="color: #9ca3af; font-size: 13px;">${dateStr}</td>
          <td style="text-align: right;">
            <button class="btn btn-secondary btn-sm" onclick='viewScorecard(${JSON.stringify(r).replace(/'/g, "&#39;")})'>Scorecard</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 24px;">No student test attempts recorded yet.</td></tr>`;
    }
  } catch (e) {
    console.error(e);
  }
}

window.viewScorecard = function(result) {
  const modal = document.getElementById('inspect-modal');
  const body = document.getElementById('inspect-modal-content');
  const title = document.getElementById('inspect-title');
  const diffBadge = document.getElementById('inspect-diff-badge');

  diffBadge.textContent = `${result.score}%`;
  diffBadge.className = result.score >= 70 ? 'lc-tag-easy' : 'lc-tag-hard';
  title.textContent = `Scorecard: ${result.user_name} — ${result.exam_name}`;

  const details = result.details || [];
  let detailsHtml = '';

  if (details.length === 0) {
    detailsHtml = '<p style="color: #9ca3af;">No question-level breakdown recorded for this submission.</p>';
  } else {
    detailsHtml = details.map((d, idx) => {
      const isCorrect = d.is_correct;
      return `
        <div style="padding: 12px; background: #242424; border: 1px solid ${isCorrect ? '#00b8a3' : '#ff375f'}; border-radius: 8px; margin-bottom: 10px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-weight: 700; color: #ffa116;">Question ${idx + 1}</span>
            <span style="font-size: 12px; font-weight: 800; color: ${isCorrect ? '#00b8a3' : '#ff375f'};">
              ${isCorrect ? '✓ CORRECT' : '✗ INCORRECT'}
            </span>
          </div>
          <div style="font-size: 13px; color: #ffffff; margin-bottom: 6px;">${escapeHtml(d.question || '')}</div>
          <div style="font-size: 12px; color: #9ca3af;">
            Student Choice: <strong>${d.selected_option !== undefined ? d.selected_option : 'Skipped'}</strong> | 
            Correct Option: <strong style="color: #00b8a3;">${d.correct_option !== undefined ? d.correct_option : 'N/A'}</strong>
          </div>
        </div>
      `;
    }).join('');
  }

  body.innerHTML = `
    <div style="display: flex; gap: 14px; margin-bottom: 16px; background: #191919; padding: 14px; border-radius: 8px; border: 1px solid #333;">
      <div><strong>Student:</strong> ${escapeHtml(result.user_name || '')} (${escapeHtml(result.user_email || '')})</div>
      <div><strong>Score:</strong> ${result.score}% (${result.correct_count}/${result.total_questions})</div>
      <div><strong>Time Taken:</strong> ${Math.round((result.time_taken_seconds || 0)/60)} mins</div>
    </div>
    <h4 style="font-size: 13px; font-weight: 700; color: #9ca3af; text-transform: uppercase; margin-bottom: 10px;">Question Breakdown:</h4>
    ${detailsHtml}
  `;

  modal.style.display = 'flex';
};

window.seedSampleQuestions = async function() {
  if (!confirm('Re-seed the entire curated 208-question database with enriched hints & solutions?')) return;
  try {
    const res = await fetch('/api/seed-sample', {method: 'POST'});
    const data = await res.json();
    if (data.ok) {
      alert(`Successfully seeded ${data.inserted} high-yield questions with multi-level hints!`);
      loadAdminQuestions();
      refreshAdminKPIs();
    } else {
      alert('Seed failed: ' + (data.error || ''));
    }
  } catch (e) {
    alert('Error seeding sample questions.');
  }
};
