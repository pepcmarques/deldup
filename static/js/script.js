const SERVER = window.location.origin;

async function fetchData(apiUrl, argument = null) {
  let url = `${SERVER}/api/${apiUrl}`;

  if (argument) {
    url += `?`;
    for (key of Object.keys(argument)) {
      url += `${key}=${argument[key]}&`;
    }
    url = url.substring(0, url.length - 1);
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const ret = await response.json();
  return ret;
}

async function previewFile(filePath) {
  const response = await fetch(`${SERVER}/api/getFile?path=${filePath}`);
  if (!response.ok) throw new Error("Failed to load file");

  const previewContainer = document.getElementById("preview");
  const contentType = response.headers.get("Content-Type");

  if (contentType.startsWith("image/")) {
    // Display image
    const imageURL = URL.createObjectURL(await response.blob());
    previewContainer.innerHTML = `<img src="${imageURL}" alt="${filePath}" style="margin-top: 10px; background-color: white; max-width: 100%; max-height: 100%;">`;
  } else if (contentType.startsWith("text/")) {
    // Display text file
    const text = await response.text();
    previewContainer.innerHTML = `<pre style="margin-top: 10px;">${text}</pre>`;
  } else if (contentType === "application/pdf") {
    // Display PDF
    const pdfURL = URL.createObjectURL(await response.blob());
    previewContainer.innerHTML = `<iframe src="${pdfURL}" style="margin-top: 10px; width: 100%; height: 600px;" frameborder="0"></iframe>`;
  } else {
    // Default for unsupported types
    previewContainer.innerHTML = `Cannot preview this file type: ${contentType}`;
  }
}

function eachDuplicate(dup) {
  return `
      <div style="margin-top: 10px;" fileid="${dup[0]}">
        <div class="row-dd">
          <img src="/static/imgs/dd.png" class="dd" fileid="${dup[0]}" filepath="${dup[1]}" alt="delete it" />
          <span style="margin-left: 5px;">${dup[1]}</span>
        </div>
      </div>`;
}

async function ddDelete(url, payload = null) {
  const body = JSON.stringify(payload);
  const response = await fetch(url, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const status = response.status;
  return status;
}

async function onDdClick(event) {
  const dd = event.target;
  const fileId = dd.getAttribute("fileid");
  const filePath = dd.getAttribute("filepath");

  let url = `${SERVER}/api/deleteFile/${fileId}`;

  const text = `Are you sure you want to delete the file below?\n${filePath}`;
  if (confirm(text) == true) {
    const status = await ddDelete(url, { filePath });
    if (status == 204) {
      const to_remove = document.querySelectorAll(`div[fileid="${fileId}"]`);
      to_remove.forEach((e) => e.remove());
      alert("File was deleted.");
    } else {
      alert("Couldn't delete the file");
    }
  }
}

async function onFileClick(event) {
  const file = event.target;
  const filePath = file.dataset.path;
  let duplicates = null;
  const message = document.getElementById("message");
  const duplicatesHtml = document.getElementById("duplicates");
  try {
    duplicates = await fetchData("findDuplicate", { path: filePath });
    duplicatesHtml.innerHTML = duplicates.duplicates.map((dup) => eachDuplicate(dup)).join("");
  } catch (error) {
    console.error("Error loading folder:", error);
  }

  if (duplicates != null && duplicates.duplicates.length > 0) {
    message.innerHTML = `${filePath} => ${duplicates.hash}`;
    document.querySelectorAll(".dd").forEach((dd) => {
      dd.addEventListener("click", onDdClick);
    });
  } else {
    message.innerHTML = "";
    duplicatesHtml.innerHTML = "<div>No duplicates for this file.</div>";
  }
  previewFile(filePath);
}

async function onFolderClick(event) {
  const folder = event.target;
  const folderPath = folder.dataset.path;
  const childrenContainer = folder.nextElementSibling;
  const level = +folder.getAttribute("level") + 1;
  if (childrenContainer.dataset.loaded === "false") {
    try {
      const children = await fetchData("directoryTree", { path: folderPath, level: level });
      childrenContainer.innerHTML = children.children
        .map((child) => renderTree(child, level, `${folderPath}`))
        .join("");
      childrenContainer.dataset.loaded = "true";
    } catch (error) {
      console.error("Error loading folder:", error);
    }
  }
  childrenContainer.classList.toggle("hidden");
  //
  document.querySelectorAll(".folder").forEach((folder) => {
    folder.addEventListener("click", onFolderClick);
  });
  //
  document.querySelectorAll(".file").forEach((file) => {
    file.addEventListener("click", onFileClick);
  });
}

function renderTree(node, level, parentPath = "") {
  const indent = level * 20; // Increase indentation for nested levels

  const nodePath = `${parentPath}/${node.name}`;

  // Render File
  if (node.type === "file") {
    return `<div class="file" level=${level} style="padding-left: ${indent}px;" data-path="${nodePath}">${node.name}</div>`;
  }

  return `
  <div>
  <div class="folder" level=${level} style="padding-left: ${indent}px;" data-path="${nodePath}">${node.name}</div>
    <div class="hidden" data-loaded="false">
    </div>
  </div>
    `;
}

// Initial render
async function openBaseDir(baseDir) {
  const root = await fetchData("directoryTree", { path: baseDir, level: 0 }); // Fetch the root node
  const tree = document.getElementById("tree");
  tree.innerHTML = `<div id="root-folder">${baseDir}</div>`;
  const level = root.level;
  tree.innerHTML += root.children.map((child) => renderTree(child, level, baseDir)).join("");

  document.querySelectorAll(".folder").forEach((folder) => {
    folder.addEventListener("click", onFolderClick);
  });
  //
  document.querySelectorAll(".file").forEach((file) => {
    file.addEventListener("click", onFileClick);
  });
}

(async function home() {
  const result = await fetchData("home");
  openBaseDir(result.baseDir);
})();
