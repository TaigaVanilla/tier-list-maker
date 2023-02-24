window.addEventListener('load', function () {
    displayMode();
}, false);

function addRow() {
    let table = document.getElementById('table');
    let row = table.insertRow(-1);
    let cell1 = row.insertCell(-1);
    let cell2 = row.insertCell(-1);
    let cell3 = row.insertCell(-1);
    cell1.innerHTML = '<input type="number" class="input-text" name="rank" max="99999">';
    cell2.innerHTML = '<input type="text" class="input-text" name="content" maxlength="80">';
    cell3.innerHTML = '<input type="text" class="input-text" name="comment" maxlength="255">';
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