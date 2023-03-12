window.addEventListener('load', function () {
    displayMode();
}, false);

function addRow() {
    let table = document.getElementById('table');
    let row = table.insertRow(-1);
    let rankCell = row.insertCell(-1);
    let contentCell = row.insertCell(-1);
    let commentCell = row.insertCell(-1);
    let rowCount = table.tBodies[0].rows.length;
    rankCell.innerHTML = `<input class="input-text" id="rank-${rowCount - 1}" max="99999" min="0" name="rank-${rowCount - 1}" size="5" type="number">`;
    contentCell.innerHTML = `<input class="input-text" id="content-${rowCount - 1}" maxlength="80" name="content-${rowCount - 1}" type="text">`;
    commentCell.innerHTML = `<input class="input-text" id="comment-${rowCount - 1}" maxlength="255" name="comment-${rowCount - 1}" type="text">`;
}

function deleteEmptyRow() {
    let table = document.getElementById('table');
    let tbl_tr = table.querySelectorAll('tr');

    let targetRowIndexList = [];

    for (let rowIndex = 1; rowIndex < tbl_tr.length; rowIndex++) {
        let cells = tbl_tr[rowIndex].querySelectorAll('td');
        if (cells[0].firstElementChild.value.trim() === '' && cells[1].firstElementChild.value.trim() === '' && cells[2].firstElementChild.value.trim() === '') {
            targetRowIndexList.push(rowIndex);
        }
    }
    for (let rowIndex = tbl_tr.length - 1; rowIndex > 1; rowIndex--) {
        if (targetRowIndexList.indexOf(rowIndex) !== -1) {
            table.deleteRow(rowIndex);
        }
    }
}

function editMode() {
    const addRowButton = document.getElementById('addRowButton');
    addRowButton.style.display = '';

    const editButton = document.getElementById('editButton');
    editButton.style.display = 'none';

    const cancelButton = document.getElementById('cancelButton');
    cancelButton.style.display = '';

    const doneButton = document.getElementById('doneButton');
    doneButton.style.display = '';

    // enable textbox to input
    const input = document.getElementsByClassName('input-text');
    for (let i = 0; i < input.length; i++) {
        input[i].classList.remove('input-disabled');
    }
}

function displayMode() {
    const addRowButton = document.getElementById('addRowButton');
    addRowButton.style.display = 'none';

    const editButton = document.getElementById('editButton');
    editButton.style.display = '';

    const cancelButton = document.getElementById('cancelButton');
    cancelButton.style.display = 'none';

    const doneButton = document.getElementById('doneButton');
    doneButton.style.display = 'none';

    // disable textbox to input
    const input = document.getElementsByClassName('input-text');
    for (let i = 0; i < input.length; i++) {
        input[i].classList.add('input-disabled');
    }
}

function showConfirm() {
    if (window.confirm('Are you sure?')) {
        document.listform.reset();
        deleteEmptyRow();
        displayMode();
    }
}