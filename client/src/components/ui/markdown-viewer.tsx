"use client"

import { memo } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import { cn } from '@/lib/utils'

interface MarkdownViewerProps {
  content: string
  className?: string
  compact?: boolean
}

const MarkdownViewer = memo(({ content, className, compact = false }: MarkdownViewerProps) => {
  return (
    <div className={cn(
      "markdown-viewer prose prose-sm dark:prose-invert max-w-none",
      "space-y-4",
      compact ? "text-sm" : "text-base",
      className
    )}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          // Headers with better spacing and hierarchy
          h1: ({ children }) => (
            <h1 className={cn(
              "font-bold text-foreground mb-4 pb-3 border-b-2 border-primary/30",
              compact ? "text-lg mt-6" : "text-2xl mt-8"
            )}>
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className={cn(
              "font-bold text-foreground mb-3 pb-2 border-b border-primary/20",
              compact ? "text-base mt-5" : "text-xl mt-6"
            )}>
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className={cn(
              "font-semibold text-foreground mb-2 text-primary",
              compact ? "text-sm mt-4" : "text-lg mt-5"
            )}>
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className={cn(
              "font-medium text-foreground mb-2 italic",
              compact ? "text-sm mt-3" : "text-base mt-4"
            )}>
              {children}
            </h4>
          ),
          
          // Paragraphs with improved spacing
          p: ({ children }) => (
            <p className={cn(
              "text-foreground leading-relaxed",
              "mb-4 last:mb-0",
              compact ? "text-sm" : "text-base"
            )}>
              {children}
            </p>
          ),
          
          // Lists with better visual separation
          ul: ({ children }) => (
            <ul className={cn(
              "list-disc list-outside mb-4 space-y-2 text-foreground",
              "marker:text-primary marker:font-bold",
              "pl-6"
            )}>
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className={cn(
              "list-decimal list-outside mb-4 space-y-2 text-foreground",
              "marker:text-primary marker:font-bold",
              "pl-6"
            )}>
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className={cn(
              "text-foreground leading-relaxed",
              compact ? "text-sm" : "text-base"
            )}>
              {children}
            </li>
          ),
          
          // Code with improved styling
          code: ({ children, className }) => {
            const isBlockCode = Boolean(className?.includes('language-'))

            if (!isBlockCode) {
              return (
                <code className={cn(
                  "bg-muted/80 px-2 py-0.5 rounded-md text-sm font-mono",
                  "text-primary border border-primary/20",
                  "inline-block"
                )}>
                  {children}
                </code>
              )
            }
            return (
              <pre className="bg-muted/50 p-4 rounded-lg text-sm font-mono overflow-x-auto mb-4 border border-primary/10">
                <code className={cn("text-foreground", className)}>
                  {children}
                </code>
              </pre>
            )
          },
          
          // Code blocks
          pre: ({ children }) => (
            <pre className="bg-muted/50 p-4 rounded-lg mb-4 overflow-x-auto border border-primary/10">
              {children}
            </pre>
          ),
          
          // Block quotes with better styling
          blockquote: ({ children }) => (
            <div className={cn(
              "bg-primary/5 border-l-4 border-primary pl-4 pr-4 py-3 italic",
              "text-muted-foreground rounded-r-md my-4",
              "dark:bg-primary/10"
            )}>
              {children}
            </div>
          ),
          
          // Tables with better styling
          table: ({ children }) => (
            <div className="overflow-x-auto mb-4 rounded-lg border border-border">
              <table className={cn(
                "min-w-full text-sm",
                "border-collapse"
              )}>
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-muted/60 border-b-2 border-primary/20">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody>
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="border-b border-border/50 hover:bg-muted/30 transition-colors">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th className={cn(
              "px-4 py-2.5 text-left font-semibold text-foreground",
              "border-r border-border/30 last:border-r-0"
            )}>
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className={cn(
              "px-4 py-2 text-foreground",
              "border-r border-border/30 last:border-r-0"
            )}>
              {children}
            </td>
          ),
          
          // Horizontal rule
          hr: () => (
            <hr className="border-border/50 my-6" />
          ),
          
          // Links with better styling
          a: ({ href, children }) => (
            <a 
              href={href}
              className={cn(
                "text-primary hover:text-primary/80 underline underline-offset-2",
                "transition-colors font-medium"
              )}
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),
          
          // Strong and emphasis
          strong: ({ children }) => (
            <strong className="font-bold text-foreground">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic">
              {children}
            </em>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
})

MarkdownViewer.displayName = 'MarkdownViewer'

export { MarkdownViewer }