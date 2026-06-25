# Student_registry_qrcode
Details of student with their unique QR or Barcode IDs - <a href="https://studentregitryqrcode-gxiczbnhqnapm3taxufzjh.streamlit.app/">Link</a>
<h3>🔍 What does it do?</h3><br>
<ol>
  <li>NumPy Structured Database: Student profiles are stored in a custom-structured NumPy array (np.dtype). By leveraging NumPy's vectorised searching (np.where), profile lookups are performed instantly without traditional database overhead.</li>
  <li>Real-time Webcam Scanner & Decoder: Integrated a hybrid computer vision scanner using OpenCV and pyzbar. Students can hold their physical QR or Barcode ID cards up to their webcam, and the app isolates, decodes, and retrieves their profile report card in real-time.</li>
  <li>	Dynamic Custom Code Generator: Generates high-definition QR codes and Code 128 barcodes. Using NumPy grid manipulation, it analyzes pixel densities to output exact percentages of dark modules.</li>
  <li>Data Analytics & Exporting: Visualizes department splits and grades using custom dark-theme Matplotlib charts. Integrated Pandas to handle seamless conversions and enable one-click database CSV downloads.</li>
  <li>Premium Glassmorphic UI: Wrapped in a modern, neon-accented dark theme built using Streamlit and custom CSS, featuring responsive layouts and custom-rendered SVG avatars.
</li>
</ol><br>
<h3>🛠️ Tech Stack & Libraries:</h3>
<ul>
  <li>Backend Storage: NumPy (Structured Arrays, Vector Indexing, Array Manipulations)
</li>
  <li>	Computer Vision & Decoding: OpenCV (cv2.QRCodeDetector), pyzbar (1D/2D Barcode Decoder)
</li>
  <li>	Data Processing & Export: Pandas
</li>
  <li>	Visual Analytics: Matplotlib
</li>
  <li>	Code Generation: qrcode, python-barcode
</li>
  <li>	User Interface: Streamlit, Custom HTML/CSS (Glassmorphic layout), SVG
</li>
  <li>	Environment: Python
</li>
</ul><br>
Developing this project allowed me to dive deep into vectorised array performance, barcode decoding tolerances under different lighting conditions, and creating polished frontends that keep users engaged.
Check out the code/UI screenshots below! I would love to hear your feedback on the implementation. Let’s connect! 👇
