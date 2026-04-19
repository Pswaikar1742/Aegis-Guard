import FileUploader from './components/FileUploader'
import ForensicStream from './components/ForensicStream'

export default function Page() {
  return (
    <main>
      <h1>Aegis Guard Dashboard</h1>
      <FileUploader />
      <ForensicStream />
    </main>
  )
}
