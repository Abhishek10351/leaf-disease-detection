import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Upload, X } from "lucide-react"

export interface FileInputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange'> {
  onFileSelect?: (file: File | null) => void
  selectedFile?: File | null
  clearable?: boolean
}

const FileInput = React.forwardRef<HTMLInputElement, FileInputProps>(
  ({ className, onFileSelect, selectedFile, clearable = true, ...props }, ref) => {
    const inputRef = React.useRef<HTMLInputElement>(null)

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0] || null
      onFileSelect?.(file)
    }

    const clearFile = () => {
      if (inputRef.current) {
        inputRef.current.value = ''
      }
      onFileSelect?.(null)
    }

    const triggerFileSelect = () => {
      inputRef.current?.click()
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
        
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={triggerFileSelect}
            className="flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            Choose File
          </Button>
          
          {selectedFile && clearable && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={clearFile}
              className="h-8 w-8 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
        
        {selectedFile && (
          <div className="text-sm text-muted-foreground">
            Selected: {selectedFile.name} ({Math.round(selectedFile.size / 1024)} KB)
          </div>
        )}
      </div>
    )
  }
)
FileInput.displayName = "FileInput"

export { FileInput }