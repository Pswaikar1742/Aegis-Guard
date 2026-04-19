export default function FileUploader() {
  return (
    <div>
      <label htmlFor="file">Upload PDF</label>
      <input id="file" type="file" accept="application/pdf" />
    </div>
  )
}
