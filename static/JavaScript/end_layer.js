$('document').ready(function () {

  const SODF = ['--Choose Layer--', 'PKG', 'D3']
  const SOHF = ['--Choose Layer--', 'PKG', 'D3']
  const RTB = ['--Choose Layer--']
  const ISG = ['--Choose Layer--']
  const DTCP = ['--Choose Layer--']
  const ABC = ['--Choose Layer--']
  const EFG = ['--Choose Layer--']
  const IJK = ['--Choose Layer--']
  const MNO = ['--Choose Layer--']
  const XYZ = ['--Choose Layer--']
  const abc = ['--Choose Layer--']
  const efg = ['--Choose Layer--']
  const ijk = ['--Choose Layer--']
  const mno = ['--Choose Layer--']
  const xyz = ['--Choose Layer--']
  const proj_i = ['--Choose Layer--']
  const proj_ii = ['--Choose Layer--']
  const proj_iii = ['--Choose Layer--']
  const proj_iv = ['--Choose Layer--']
  const proj_v = ['--Choose Layer--']


  $('#id_project').change(function () {
    var el2 = $(this);
    var sel2 = document.querySelector('#id_layer')
    sel2.innerHTML = ""

    if (el2.val() === "Order_Details") {
      SODF.forEach((SODF) => {
        const opt = document.createElement("option");
        // opt.val(i);
        const name = document.createTextNode(SODF);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "Order_Header") {
      SOHF.forEach((SOHF) => {
        const opt = document.createElement("option");
        // opt.val(i);
        const name = document.createTextNode(SOHF);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }

    else if (el2.val() === "RTB") {
      RTB.forEach((RTB) => {
        const opt = document.createElement("option");
        // opt.val(i);
        const name = document.createTextNode(RTB);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }

    else if (el2.val() === "ISG") {
      ISG.forEach((ISG) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(ISG);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }

    else if (el2.val() === "DTCP") {
      DTCP.forEach((DTCP) => {
        const opt = document.createElement("option");
        // opt.val(i);
        const name = document.createTextNode(DTCP);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;
      });

    }
    else if (el2.val() === "ABC") {
      ABC.forEach((ABC) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(ABC);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "EFG") {
      EFG.forEach((EFG) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(EFG);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "IJK") {
      IJK.forEach((IJK) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(IJK);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "MNO") {
      MNO.forEach((MNO) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(MNO);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "XYZ") {
      XYZ.forEach((XYZ) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(XYZ);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "abc") {
      abc.forEach((abc) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(abc);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "efg") {
      efg.forEach((efg) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(efg);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "ijk") {
      ijk.forEach((ijk) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(ijk);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "mno") {
      mno.forEach((mno) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(mno);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "xyz") {
      xyz.forEach((xyz) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(xyz);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "i") {
      proj_i.forEach((proj_i) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(proj_i);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "ii") {
      proj_ii.forEach((proj_ii) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(proj_ii);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "iii") {
      proj_iii.forEach((proj_iii) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(proj_iii);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "iv") {
      proj_iv.forEach((proj_iv) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(proj_iv);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }
    else if (el2.val() === "v") {
      proj_v.forEach((proj_v) => {
        const opt = document.createElement("option");
        // opt.val(i);s
        const name = document.createTextNode(proj_v);
        opt.appendChild(name);
        sel2.appendChild(opt);
        i = i + 1;

      });
    }

  });

});