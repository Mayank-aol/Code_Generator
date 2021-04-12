$('document').ready(function () {

    // const 
    $('#id_num_col').change(function () {

        var ele = $(this);
        var n = ele.val();
        console.log(n);
        var tab = document.querySelector('#id_col_table');
        var tbody = tab.children[0];
        tbody.innerHTML = ''

        for (i = 0; i < n; i++) {
            // var a = parseint(i)
            const tr1 = document.createElement('tr');
            const tr2 = document.createElement('tr');
            const tr3 = document.createElement('tr');
            tbody.appendChild(tr1);
            tbody.appendChild(tr2);
            tbody.appendChild(tr3);
            const td1a = document.createElement('td');
            const td1b = document.createElement('td');
            const lab1 = document.createElement('label');
            lab1.setAttribute('for', '#id_col_name_' + (i + 1));
            lab1.innerText = 'Enter Name of Column_' + (i + 1) + ' :';
            td1a.appendChild(lab1);
            tr1.appendChild(td1a);
            tr1.appendChild(td1b);
            const inp1 = document.createElement('input');
            inp1.setAttribute('type', 'text');
            inp1.setAttribute('name', 'name_col_' + (i + 1));
            inp1.setAttribute('id', 'id_col_name' + (i + 1));
            td1b.appendChild(inp1);
            const td2a = document.createElement('td');
            const td2b = document.createElement('td');
            const lab2 = document.createElement('label');
            lab2.setAttribute('for', '#id_col_dt_' + (i + 1));
            lab2.innerText = 'Enter Datatype for the Column_' + (i + 1) + ' :';
            td2a.appendChild(lab2);
            tr2.appendChild(td2a);
            tr2.appendChild(td2b);
            const inp2 = document.createElement('input');
            inp2.setAttribute('type', 'text');
            inp2.setAttribute('name', 'dt_col_' + (i + 1));
            inp2.setAttribute('id', 'id_col_dt_' + (i + 1));
            td2b.appendChild(inp2);
            // td2.appendChild()
        }

    });

});