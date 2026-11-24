(() => {
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const entries = [...document.querySelectorAll('.blog-entry')];
  const years = [...document.querySelectorAll('.blog-year')];
  const status = document.querySelector('.filter-status');
  function filter(tag, push = false) {
    if (!buttons.some(button => button.dataset.filter === tag)) tag = 'all';
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = tag !== 'all' && !entry.dataset.tags.split(' ').includes(tag);
      if (!entry.hidden) count++;
    });
    years.forEach(year => {
      year.hidden = ![...year.querySelectorAll('.blog-entry')].some(entry => !entry.hidden);
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === tag)));
    status.textContent = `${count} ${count === 1 ? 'post' : 'posts'}${tag === 'all' ? '' : ` in ${tag[0].toUpperCase() + tag.slice(1)}`}`;
    if (push) {
      const url = new URL(location.href);
      if (tag === 'all') url.searchParams.delete('tag');
      else url.searchParams.set('tag', tag);
      history.pushState({}, '', url);
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => filter(button.dataset.filter, true)));
  document.querySelectorAll('[data-tag]').forEach(link => link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    filter(link.dataset.tag, true);
    document.querySelector('.blog-filters').scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }));
  addEventListener('popstate', () => filter(new URLSearchParams(location.search).get('tag') || 'all'));
  filter(new URLSearchParams(location.search).get('tag') || 'all');
})();
