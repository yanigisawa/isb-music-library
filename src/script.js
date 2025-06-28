
function searchForTune(e) {
  let searchValue = $("#tuneSearch").val();
  $("#results").show();
  if (searchValue === '') {
    $('#results').html('<span>Enter title, composer, or library folder location</span>');
    return
  }
  searchValue = searchValue.replaceAll(' ', '').toLowerCase();
  let filteredResults = isb_library.scores.filter(score => {
    let title = score['Title'].toLowerCase().replaceAll(' ', '');
    let composer = score['Composer'].toLowerCase().replaceAll(' ', '');
    let arranger = score['Arranger'].toLowerCase().replaceAll(' ', '');
    return (
      title.includes(searchValue) ||
      composer.includes(searchValue) ||
      arranger.includes(searchValue) ||
      score['Library ID'].toLowerCase().includes(searchValue)
    );

  })
  filteredResults = filteredResults.sort((item1, item2) => {
    return item1['Title'].localeCompare(item2['Title'], 'en', { sensitivity: 'base' });
  }).map(tune => {
    let regEx = new RegExp(searchValue, "ig");
    let composer = tune.Composer;
    if (tune.Arranger !== "") {
      composer += ` (Arr: ${tune.Arranger})`;
    }
    composer = composer.replaceAll(regEx , "<span class='highlight'>$&</span>");
    return {
      Title: tune.Title.replaceAll(regEx , "<span class='highlight'>$&</span>"),
      Composer: composer,
      "Library ID": tune['Library ID'].replaceAll(regEx , "<span class='highlight'>$&</span>"),
    }
  });
  var e, html, json, template;
  try {
    template = $('#template').html();
    json = {
      empty: filteredResults.length === 0,
      items: filteredResults.slice(0, 50),
      itemCount: filteredResults.length,
      extraText: filteredResults.length > 50 ? '(First 50 shown)' : '',
    }

    html = Mustache.to_html(template, json).replace(/^\s*/mg, '');
  } catch (_error) {
    e = _error;
    html = e.toString();
  }
  $('#results').html(html);
}

$(function () {
  $("#tuneSearch").on('input', searchForTune);
  $("#tuneSearch").on('focus blur', () => {
    $(".hideWhenSearching").toggle();
  });

});

$(document).on('touchmove', function(e) {
    e.preventDefault();
});
