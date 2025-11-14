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
      "markdown-viewer",
      compact ? "text-sm" : "text-base",
      className
    )}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          // Headers
          h1: ({ children }) => (
            <h1 className={cn(
              "font-bold text-foreground mb-4 pb-2 border-b",
              compact ? "text-lg" : "text-2xl"
            )}>
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className={cn(
              "font-bold text-foreground mb-3 mt-6",
              compact ? "text-base" : "text-xl"
            )}>
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className={cn(
              "font-semibold text-foreground mb-2 mt-4",
              compact ? "text-sm" : "text-lg"
            )}>
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className={cn(
              "font-medium text-foreground mb-2 mt-3",
              compact ? "text-sm" : "text-base"
            )}>
              {children}
            </h4>
          ),
          
          // Paragraphs
          p: ({ children }) => (
            <p className="text-foreground mb-4 leading-relaxed last:mb-0">
              {children}
            </p>
          ),
          
          // Lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-4 space-y-1 text-foreground ml-4">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-4 space-y-1 text-foreground ml-4">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="text-foreground leading-relaxed">
              {children}
            </li>
          ),
          
          // Code
          code: ({ inline, children, className }) => {
            if (inline) {
              return (
                <code className="bg-muted px-1.5 py-0.5 rounded-md text-sm font-mono text-foreground">
                  {children}
                </code>
              )
            }
            return (
              <code className={cn("block bg-muted p-4 rounded-lg text-sm font-mono overflow-x-auto", className)}>
                {children}
              </code>
            )
          },
          
          // Code blocks
          pre: ({ children }) => (
            <pre className="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
              {children}
            </pre>
          ),
          
          // Block quotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-primary pl-4 italic text-muted-foreground mb-4">
              {children}
            </blockquote>
          ),
          
          // Tables
          table: ({ children }) => (
            <div className="overflow-x-auto mb-4">
              <table className="min-w-full border-collapse border border-border">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-muted">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody>
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="border-b border-border">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th className="border border-border px-4 py-2 text-left font-semibold text-foreground">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-border px-4 py-2 text-foreground">
              {children}
            </td>
          ),
          
          // Horizontal rule
          hr: () => (
            <hr className="border-border my-6" />
          ),
          
          // Links
          a: ({ href, children }) => (
            <a 
              href={href}
              className="text-primary hover:text-primary/80 underline underline-offset-2"
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
            <em className="italic text-foreground">
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