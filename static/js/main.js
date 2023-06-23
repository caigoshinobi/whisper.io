// Function to perform the search
function searchBooks() {
    var keywords = document.getElementById('search-input').value.toLowerCase();
    $.ajax({
        url: '/api/search',
        type: 'POST',
        data: { keywords: keywords },
        success: function (response) {
            var booksContainer = document.getElementById('books-container');
            booksContainer.innerHTML = response.map(function (book) {
                return `
            <div class="col-md-3 mb-3">
                <div class="card" onclick="location.href='/player/${book.id}';" style="cursor: pointer;">
                <img src="${book.cover}" class="card-img-top book-cover" alt="Cover">
                <div class="card-body">
                    <h5 class="card-title">${book.title}</h5>
                    <p class="card-text">${book.author}</p>
                </div>
                </div>
            </div>
            `;
            }).join('');
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Search button click event
$('#search-button').on('click', function () {
    searchBooks();
});

// Enter key press event in the search box
$('#search-input').on('keypress', function (e) {
    if (e.which === 13) {
        e.preventDefault();
        searchBooks();
    }
});

// Aggiorna il testo della label dell'audio quando viene selezionato un file
$('#audio').on('change', function() {
    var file = $(this).prop('files')[0];
    $('#audio-label').text(file.name);
  });

// Aggiorna il testo della label quando vengono selezionati i file
$('#cover').on('change', function() {
    var files = $(this).prop('files');
    var fileNames = [];
  
    for (var i = 0; i < files.length; i++) {
      fileNames.push(files[i].name);
    }
  
    $('#cover-label').text(fileNames.join(', '));
  });