import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Upload, X, Camera } from "lucide-react"

export interface FileInputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange'> {
  onFileSelect?: (file: File | null) => void
  selectedFile?: File | null
  clearable?: boolean
  showCameraButton?: boolean
  cameraCapture?: "user" | "environment"
  cameraLabel?: string
}

const FileInput = React.forwardRef<HTMLInputElement, FileInputProps>(
  (
    {
      className,
      onFileSelect,
      selectedFile,
      clearable = true,
      showCameraButton = false,
      cameraCapture = "environment",
      cameraLabel = "Take Photo",
      ...props
    },
    ref
  ) => {
    const inputRef = React.useRef<HTMLInputElement>(null)
    const cameraInputRef = React.useRef<HTMLInputElement>(null)

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0] || null
      onFileSelect?.(file)
    }

    const handleCameraChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0] || null
      onFileSelect?.(file)
    }

    const clearFile = () => {
      if (inputRef.current) {
        inputRef.current.value = ''
      }
      if (cameraInputRef.current) {
        cameraInputRef.current.value = ''
      }
      onFileSelect?.(null)
    }

    const triggerFileSelect = () => {
      inputRef.current?.click()
    }

    const triggerCameraCapture = () => {
      cameraInputRef.current?.click()
    }

    React.useImperativeHandle(ref, () => inputRef.current!)

    return (
      <div className={cn("space-y-2", className)}>
        <Input
          ref={inputRef}
          type="file"
          onChange={handleFileChange}
          className="hidden"
          {...props}
        />

        {showCameraButton && (
          <Input
            ref={cameraInputRef}
            type="file"
            accept="image/*"
            capture={cameraCapture}
            onChange={handleCameraChange}
            className="hidden"
          />
        )}
        
        <div className="flex flex-col sm:flex-row sm:items-center gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={triggerFileSelect}
            className="flex items-center gap-2 w-full sm:w-auto"
          >
            <Upload className="h-4 w-4" />
            Choose File
          </Button>

          {showCameraButton && (
            <Button
              type="button"
              variant="outline"
              onClick={triggerCameraCapture}
              className="flex items-center gap-2 w-full sm:w-auto"
            >
              <Camera className="h-4 w-4" />
              {cameraLabel}
            </Button>
          )}
          
          {selectedFile && clearable && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={clearFile}
              className="h-8 w-8 p-0 self-start sm:self-auto"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
        
        {selectedFile && (
          <div className="text-sm text-muted-foreground break-all">
            Selected: {selectedFile.name} ({Math.round(selectedFile.size / 1024)} KB)
          </div>
        )}
      </div>
    )
  }
)
FileInput.displayName = "FileInput"

export { FileInput }