export interface NavigationItem {
    href: string;
    label: string;
}

export interface FormData {
    id: string;
    name: string;
    description?: string;
    fields: FormField[];
    createdAt: Date;
    updatedAt: Date;
}

export interface FormField {
    id: string;
    type:
        | "text"
        | "email"
        | "number"
        | "select"
        | "textarea"
        | "checkbox"
        | "radio"
        | "date"
        | "file"
        | "rating";
    label: string;
    placeholder?: string;
    required: boolean;
    options?: string[]; // for select, checkbox, radio fields
    validation?: {
        min?: number;
        max?: number;
        pattern?: string;
    };
}
