
document.addEventListener('click',function(e){
  const tab=e.target.closest('.tab-button');
  if(tab){
    const wrap=tab.closest('.tabs');
    wrap.querySelectorAll('.tab-button').forEach(b=>b.classList.remove('active'));
    wrap.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
    tab.classList.add('active');
    wrap.querySelector('#'+tab.dataset.tab).classList.add('active');
  }
  const hamb=e.target.closest('#hamburger');
  if(hamb){document.querySelector('#mobilePanel')?.classList.toggle('open')}
});


(function(){
  function applyLang(lang){
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('.i18n').forEach(function(el){
      var value = el.getAttribute(lang === 'en' ? 'data-en' : 'data-zh');
      if(value !== null){ el.innerHTML = value; }
    });
    document.querySelectorAll('[data-ph-zh],[data-ph-en]').forEach(function(el){
      var value = el.getAttribute(lang === 'en' ? 'data-ph-en' : 'data-ph-zh');
      if(value !== null){ el.setAttribute('placeholder', value); }
    });
    document.querySelectorAll('[data-set-lang]').forEach(function(btn){
      btn.classList.toggle('active', btn.getAttribute('data-set-lang') === lang);
    });
    var title = document.body.getAttribute(lang === 'en' ? 'data-title-en' : 'data-title-zh');
    if(title){ document.title = title; }
    try{ localStorage.setItem('fdlLang', lang); }catch(e){}
  }
  document.addEventListener('click', function(e){
    var btn = e.target.closest('[data-set-lang]');
    if(btn){ applyLang(btn.getAttribute('data-set-lang')); }
  });
  document.addEventListener('DOMContentLoaded', function(){
    var saved='zh';
    try{ saved=localStorage.getItem('fdlLang') || 'zh'; }catch(e){}
    applyLang(saved === 'en' ? 'en' : 'zh');
  });
})();

// Handle quote form submission
document.addEventListener('submit', function(e) {
  const quoteForm = e.target.closest('.quote-form');
  if (quoteForm) {
    e.preventDefault();
    var currentLang = 'zh';
    try { currentLang = localStorage.getItem('fdlLang') || 'zh'; } catch(err) {}

    const nameVal = (quoteForm.querySelector('[name="name"]') || {}).value || '';
    const emailVal = (quoteForm.querySelector('[name="email"]') || {}).value || '';
    const whatsappVal = (quoteForm.querySelector('[name="whatsapp"]') || {}).value || '';
    const messageVal = (quoteForm.querySelector('[name="message"]') || {}).value || '';

    if (!nameVal.trim() || !emailVal.trim() || !whatsappVal.trim()) {
      alert(currentLang === 'en' ? 'Please fill in all required fields.' : '请填写所有必填字段。');
      return;
    }

    const submitBtn = quoteForm.querySelector('button[type="submit"]');
    const originalBtnHtml = submitBtn ? submitBtn.innerHTML : 'Submit';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = currentLang === 'en' ? 'Submitting...' : '提交中...';
    }

    fetch('https://formsubmit.co/ajax/liujunpeng@hzgjgc.com', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        _subject: 'New Inquiry from FDL SORT Product Page',
        'Name or Company Name': nameVal,
        'Email Address': emailVal,
        'WhatsApp Number': whatsappVal,
        'Material stream / capacity / purity target': messageVal
      })
    })
    .then(response => response.ok ? response.json() : Promise.reject())
    .then(() => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
      quoteForm.reset();

      // Meta Lead Event Tracking (Pixel & CAPI Deduplication)
      if (typeof fbq === 'function') {
        const leadEventId = 'evt_lead_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
        fbq('track', 'Lead', {}, { eventID: leadEventId });
        
        if (typeof hashMetaValue === 'function') {
          Promise.all([
            hashMetaValue(emailVal),
            hashMetaValue(whatsappVal)
          ]).then(([hashedEmail, hashedPhone]) => {
            fetch('/api/meta-capi', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                eventName: 'Lead',
                eventID: leadEventId,
                user_data: {
                  em: hashedEmail,
                  ph: hashedPhone
                }
              })
            }).catch(err => console.error('Meta CAPI Lead Error:', err));
          });
        }
      }

      alert(currentLang === 'en' ? 'Thank you! Your inquiry has been submitted successfully.' : '感谢您的咨询！您的需求已成功提交。');
    })
    .catch(() => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
      alert(currentLang === 'en' ? 'Submission failed. Please try again or contact us by email.' : '提交失败。请重试或通过电子邮件联系我们。');
    });
  }
});

// 自动收起二级页面移动端菜单
document.addEventListener('click', function(e) {
  const link = e.target.closest('#mobilePanel a');
  if (link) {
    document.querySelector('#mobilePanel')?.classList.remove('open');
  }
});

