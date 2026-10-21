(function () {
  document.addEventListener('DOMContentLoaded', function () {
    ['objective-grid', 'stakeholder-grid'].forEach(function (selector) {
      document.querySelectorAll('.' + selector).forEach(function (grid) {
        var items = grid.querySelectorAll(':scope > div');
        var count = items.length;
        if (!count) {
          return;
        }

        var maxColumns = 4;
        var rows = Math.ceil(count / maxColumns);
        var cols = Math.ceil(count / rows);

        grid.style.gridTemplateColumns = 'repeat(' + cols + ', 1fr)';
      });
    });
  });
})();
