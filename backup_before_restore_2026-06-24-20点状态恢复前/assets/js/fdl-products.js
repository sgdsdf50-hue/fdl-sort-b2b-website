
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
