/**
 * pipeline.js - Big Data Pipeline & Infrastructure Controller
 */

async function loadPipelineStatus() {
  try {
    const res = await fetch("/api/pipeline-status");
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderSystemCards(json.data);
    }
  } catch (e) {
    console.error("Pipeline status error:", e);
  }
}

function renderSystemCards(data) {
  // Python Card
  const pyBadge = document.getElementById("status-python-badge");
  const pyDetails = document.getElementById("status-python-details");
  if (pyBadge) pyBadge.innerHTML = `<span class="status-pill status-connected"><span class="status-dot"></span> ${data.python.status}</span>`;
  if (pyDetails) pyDetails.innerText = `${data.python.version} • ${data.python.details}`;

  // Hadoop Card
  const hadoopBadge = document.getElementById("status-hadoop-badge");
  const hadoopDetails = document.getElementById("status-hadoop-details");
  const isHadoop = data.hadoop.installed;
  if (hadoopBadge) hadoopBadge.innerHTML = `<span class="status-pill ${isHadoop ? 'status-connected' : 'status-disconnected'}"><span class="status-dot"></span> ${data.hadoop.status}</span>`;
  if (hadoopDetails) hadoopDetails.innerText = data.hadoop.details;

  // HDFS Card
  const hdfsBadge = document.getElementById("status-hdfs-badge");
  const hdfsDetails = document.getElementById("status-hdfs-details");
  const isHdfs = data.hdfs.available;
  if (hdfsBadge) hdfsBadge.innerHTML = `<span class="status-pill ${isHdfs ? 'status-connected' : 'status-disconnected'}"><span class="status-dot"></span> ${data.hdfs.status}</span>`;
  if (hdfsDetails) hdfsDetails.innerText = data.hdfs.details;

  // Hive Card
  const hiveBadge = document.getElementById("status-hive-badge");
  const hiveDetails = document.getElementById("status-hive-details");
  const isHive = data.hive.installed;
  if (hiveBadge) hiveBadge.innerHTML = `<span class="status-pill ${isHive ? 'status-connected' : 'status-disconnected'}"><span class="status-dot"></span> ${data.hive.status}</span>`;
  if (hiveDetails) hiveDetails.innerText = data.hive.details;

  // MongoDB Card
  const mongoBadge = document.getElementById("status-mongo-badge");
  const mongoDetails = document.getElementById("status-mongo-details");
  const isMongo = data.mongodb.connected;
  if (mongoBadge) mongoBadge.innerHTML = `<span class="status-pill ${isMongo ? 'status-connected' : 'status-disconnected'}"><span class="status-dot"></span> ${data.mongodb.status}</span>`;
  if (mongoDetails) mongoDetails.innerText = data.mongodb.details;

  // Dataset Card
  const dataBadge = document.getElementById("status-dataset-badge");
  const dataDetails = document.getElementById("status-dataset-details");
  const isData = data.dataset.status === "LOADED / READY";
  if (dataBadge) dataBadge.innerHTML = `<span class="status-pill ${isData ? 'status-connected' : 'status-disconnected'}"><span class="status-dot"></span> ${data.dataset.status}</span>`;
  if (dataDetails) dataDetails.innerText = `Raw: ${data.dataset.raw_present ? 'Present' : 'Missing'} • Cleaned: ${data.dataset.cleaned_present ? 'Ready' : 'Missing'}`;
}

async function triggerCleaning() {
  const btn = document.getElementById("btn-trigger-cleaning");
  const statusMsg = document.getElementById("pipeline-action-msg");
  if (btn) btn.disabled = true;
  if (statusMsg) statusMsg.innerHTML = '<span style="color:#F59E0B;">⏳ Running Python Data Cleaning Pipeline...</span>';

  try {
    const res = await fetch("/api/pipeline/clean", { method: "POST" });
    const json = await res.json();
    if (json.success) {
      statusMsg.innerHTML = `<span style="color:#10B981;">✅ ${json.message} (Cleaned ${json.metrics.final_rows} rows)</span>`;
      loadPipelineStatus();
    } else {
      statusMsg.innerHTML = `<span style="color:#EF4444;">❌ ${json.message}</span>`;
    }
  } catch (e) {
    statusMsg.innerHTML = `<span style="color:#EF4444;">❌ Error: ${e.message}</span>`;
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function triggerMongoSync() {
  const btn = document.getElementById("btn-trigger-mongosync");
  const statusMsg = document.getElementById("pipeline-action-msg");
  if (btn) btn.disabled = true;
  if (statusMsg) statusMsg.innerHTML = '<span style="color:#F59E0B;">⏳ Ingesting Cleaned Dataset into MongoDB Atlas...</span>';

  try {
    const res = await fetch("/api/pipeline/sync-mongodb", { method: "POST" });
    const json = await res.json();
    if (json.success) {
      statusMsg.innerHTML = `<span style="color:#10B981;">✅ ${json.message}</span>`;
      loadPipelineStatus();
    } else {
      statusMsg.innerHTML = `<span style="color:#EF4444;">⚠️ ${json.message}</span>`;
    }
  } catch (e) {
    statusMsg.innerHTML = `<span style="color:#EF4444;">❌ Error: ${e.message}</span>`;
  } finally {
    if (btn) btn.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadPipelineStatus();
  const cleanBtn = document.getElementById("btn-trigger-cleaning");
  const mongoBtn = document.getElementById("btn-trigger-mongosync");
  if (cleanBtn) cleanBtn.addEventListener("click", triggerCleaning);
  if (mongoBtn) mongoBtn.addEventListener("click", triggerMongoSync);
});
