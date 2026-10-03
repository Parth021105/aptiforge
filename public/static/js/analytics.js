document.addEventListener('DOMContentLoaded', async () => {
  const accEl = document.getElementById('ana-acc');
  const avgScoreEl = document.getElementById('ana-avg-score');
  const examsEl = document.getElementById('ana-exams');
  const weakCntEl = document.getElementById('ana-weak-cnt');

  const topicBarsContainer = document.getElementById('topic-bars-container');
  const weakTopicsList = document.getElementById('weak-topics-list');
  const historyTbody = document.getElementById('exam-history-tbody');

  try {
    const res = await fetch('/api/student/analytics');
    const data = await res.json();

    if (data.ok && data.summary) {
      const s = data.summary;

      accEl.textContent = `${s.practice_accuracy || 0}%`;
      avgScoreEl.textContent = `${s.avg_score || 0}%`;
      examsEl.textContent = s.total_exams || 0;
      weakCntEl.textContent = (s.weak_topics || []).length;

      // Render Topic Mastery Bars
      renderTopicBars(s.topic_stats || []);

      // Render Weak Topics
      renderWeakTopics(s.weak_topics || []);

      // Render Exam History
      renderExamHistory(s.recent_exams || []);
    } else {
      topicBarsContainer.innerHTML = `<p class="page-subtitle">No performance data available yet. Start practicing to generate analytics!</p>`;
      historyTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No exams taken yet.</td></tr>`;
    }
  } catch (err) {
    console.error('Error loading analytics:', err);
  }

  function renderTopicBars(topicStats) {
    if (!topicStats.length) {
      topicBarsContainer.innerHTML = `
        <div style="text-align: center; padding: 20px;">
          <p style="color: var(--text-muted);">Practice or take mock tests to calculate your topic mastery percentages!</p>
          <a href="/practice" class="btn btn-secondary btn-sm" style="margin-top: 10px;">Go to Practice Portal</a>
        </div>
      `;
      return;
    }

    topicBarsContainer.innerHTML = '';
    topicStats.forEach(item => {
      const acc = item.accuracy || 0;
      let fillClass = 'success';
      if (acc < 65) fillClass = 'danger';
      else if (acc < 75) fillClass = '';

      const wrapper = document.createElement('div');
      wrapper.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 14px; font-weight: 600;">
          <span style="color: var(--text-main);">${item.topic}</span>
          <span style="color: ${acc >= 75 ? 'var(--accent-emerald)' : (acc < 65 ? 'var(--accent-rose)' : 'var(--accent-amber)')};">${acc}% Mastery (${item.correct}/${item.total})</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill ${fillClass}" style="width: ${acc}%;"></div>
        </div>
      `;
      topicBarsContainer.appendChild(wrapper);
    });
  }

  function renderWeakTopics(weakTopics) {
    if (!weakTopics.length) {
      weakTopicsList.innerHTML = `<p style="font-size: 13px; color: var(--accent-emerald);">🎉 Great job! No weak topics detected (all topics above 65%).</p>`;
      return;
    }

    weakTopicsList.innerHTML = '';
    weakTopics.forEach(wt => {
      const card = document.createElement('div');
      card.style.cssText = 'display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: rgba(7, 11, 20, 0.6); border-radius: 8px; border: 1px solid rgba(251, 113, 133, 0.2);';
      card.innerHTML = `
        <div>
          <div style="font-size: 13px; font-weight: 700; color: var(--text-main);">${wt.topic}</div>
          <div style="font-size: 11px; color: var(--accent-rose);">${wt.accuracy}% Accuracy</div>
        </div>
        <a href="/practice?topic=${encodeURIComponent(wt.topic)}" class="btn btn-ghost btn-sm">Practice ➔</a>
      `;
      weakTopicsList.appendChild(card);
    });
  }

  function renderExamHistory(recentExams) {
    if (!recentExams.length) {
      historyTbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No mock exams completed yet.</td></tr>`;
      return;
    }

    historyTbody.innerHTML = '';
    recentExams.forEach(ex => {
      const score = ex.score || 0;
      const tr = document.createElement('tr');

      const secs = ex.time_taken_seconds || 0;
      const m = Math.floor(secs / 60);
      const s = secs % 60;
      const timeStr = secs ? `${m}m ${s}s` : 'N/A';

      const dateStr = ex.created_at ? new Date(ex.created_at).toLocaleDateString() : 'Today';

      tr.innerHTML = `
        <td style="font-weight: 600;">${ex.exam_name || 'Mock Aptitude Exam'}</td>
        <td style="font-weight: 700; color: ${score >= 75 ? 'var(--accent-emerald)' : (score < 60 ? 'var(--accent-rose)' : 'var(--accent-amber)')};">${score}%</td>
        <td>${ex.correct_count || 0} / ${ex.total_questions || 0}</td>
        <td>${timeStr}</td>
        <td>${dateStr}</td>
        <td><span class="badge ${score >= 75 ? 'badge-easy' : (score < 60 ? 'badge-hard' : 'badge-medium')}">${score >= 75 ? 'PASSED' : (score < 60 ? 'NEEDS IMPROVEMENT' : 'AVERAGE')}</span></td>
      `;
      historyTbody.appendChild(tr);
    });
  }
});
