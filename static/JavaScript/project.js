$(document).ready(function () {

    const Orders = ['--Choose Project--', 'Order_Header', 'Order_Details', 'RTB', 'ISG', 'DTCP']
    const Doms = ['--Choose Project--', 'ABC', 'EFG', 'IJK', 'MNO', 'XYZ']
    const Finance = ['--Choose Project--', 'abc', 'efg', 'ijk', 'mno', 'xyz']
    const DevOps = ['--Choose Project--', 'i', 'ii', 'iii', 'iv', 'v']

    $("#id_team").change(function () {

        var el = $(this);
        var sel1 = document.querySelector('#id_project');
        sel1.innerHTML = "";
        i = 0;
        if (el.val() === "OrdnProd") {
            Orders.forEach((Orders) => {
                const opt = document.createElement("option");
                // opt.val(i);
                const name = document.createTextNode(Orders);
                opt.appendChild(name);
                sel1.appendChild(opt);
                i = i + 1;

            });
        }
        else if (el.val() === "Doms") {
            Doms.forEach((Doms) => {
                const opt = document.createElement("option");
                // opt.val(i);
                const name = document.createTextNode(Doms);
                opt.appendChild(name);
                sel1.appendChild(opt);
                i = i + 1;

            });
        }

        else if (el.val() === "Fin") {
            Finance.forEach((Finance) => {
                const opt = document.createElement("option");
                // opt.val(i);
                const name = document.createTextNode(Finance);
                opt.appendChild(name);
                sel1.appendChild(opt);
                i = i + 1;

            });
        }

        else if (el.val() === "DevOps") {
            DevOps.forEach((DevOps) => {
                const opt = document.createElement("option");
                // opt.val(i);s
                const name = document.createTextNode(DevOps);
                opt.appendChild(name);
                sel1.appendChild(opt);
                i = i + 1;

            });
        }
    });

});