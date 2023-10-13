var j = 1;
function handleFiles(files) {
      var d = document.getElementById("new_div"+j);

      var button = document.createElement("button");

    // ✅ Set Attributes on Element
      button.setAttribute('id', "iclear"+j);
//      button.setAttribute('name', "iclear"+j);
      button.setAttribute('type', "button");
      button.setAttribute('class', "btn btn-danger");
    // ✅ Add text content to element
      button.textContent = 'X';


      if (!files.length) {
        d.innerHTML = "<p>No files selected!</p>";
      } else {
        for (var i=0; i < files.length; i++) {

          var img = document.createElement("img");
          img.src = window.URL.createObjectURL(files[i]);;
          img.height = 350;
          img.width = 350;
          img.onload = function() {
            window.URL.revokeObjectURL(this.src);
          }

          d.appendChild(button);
          d.appendChild(img);

        }
      }
      j++;
    }




//function handleFiles(files) {
//      var d = document.getElementById("roww"+j);
////      var d = document.getElementsByClassName("input-group m-3");
//
//      if (!files.length) {
//        d.innerHTML = "<p>No files selected!</p>";
//      } else {
//        for (var i=0; i < files.length; i++) {
//
//          var img = document.createElement("img");
//          img.src = window.URL.createObjectURL(files[i]);;
//          img.height = 350;
//          img.width = 350;
//          img.onload = function() {
//            window.URL.revokeObjectURL(this.src);
//          }
//          d.appendChild(img);
//
////          var info = document.createElement("li")
////          info.innerHTML = files[i].name + ": " + files[i].size + " bytes"
////          info.innerHTML = files[i].name
////          d.appendChild(info)
//        }
//      }
//      j++;
//    }