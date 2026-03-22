import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useDropzone } from "react-dropzone"
import { UploadCloud, X } from "lucide-react"

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

    const parseAccept = React.useMemo(() => {
      if (!props.accept) return undefined
      return props.accept
        .split(",")
        .map((entry) => entry.trim())
        .filter(Boolean)
        .reduce<Record<string, string[]>>((acc, key) => {
          acc[key] = []
          return acc
        }, {})
    }, [props.accept])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
      multiple: false,
      accept: parseAccept,
      noClick: true,
      onDrop: (acceptedFiles) => {
        onFileSelect?.(acceptedFiles[0] ?? null)
      },
    })

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

        <div
          {...getRootProps()}
          className={cn(
            "rounded-xl border-2 border-dashed p-4 sm:p-6 text-center transition-all duration-200",
            isDragActive
              ? "border-emerald-500 bg-emerald-50"
              : "border-border bg-muted/20 hover:bg-muted/35"
          )}
        >
          <input {...getInputProps()} />
          <div className="mx-auto mb-2 sm:mb-3 flex h-9 w-9 sm:h-10 sm:w-10 items-center justify-center rounded-full bg-emerald-100 text-emerald-700">
            <UploadCloud className="h-4 w-4 sm:h-5 sm:w-5" />
          </div>
          <p className="text-sm font-medium text-foreground">
            {isDragActive ? "Drop image here" : "Drag & drop an image"}
          </p>
          <p className="mt-1 text-xs text-muted-foreground">
            or choose one from your device
          </p>

          <div className="mt-3 sm:mt-4 flex flex-col gap-2 sm:flex-row sm:justify-center">
            <Button
              type="button"
              variant="outline"
              onClick={triggerFileSelect}
              size="sm"
              className="w-full sm:w-auto"
            >
              Browse Files
            </Button>

            {showCameraButton && (
              <Button
                type="button"
                variant="outline"
                onClick={triggerCameraCapture}
                size="sm"
                className="w-full sm:w-auto"
              >
                {cameraLabel}
              </Button>
            )}
          </div>
        </div>

        <div className="flex items-center justify-end">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={clearFile}
            className={cn("h-8 w-8 p-0", !selectedFile || !clearable ? "invisible" : "")}
            aria-label="Clear selected file"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        {selectedFile && (
          <div className="rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-900 break-all border border-emerald-100">
            {selectedFile.name} ({Math.round(selectedFile.size / 1024)} KB)
          </div>
        )}
      </div>
    )
  }
)
FileInput.displayName = "FileInput"

export { FileInput }