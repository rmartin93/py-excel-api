```tsx
"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Skeleton } from "@/components/ui/skeleton";
import { Plus, Pencil, Trash2 } from "lucide-react";

interface AdminNote {
	id: string;
	author: string;
	authorInitials: string;
	content: string;
	timestamp: string;
}

const mockNotes: AdminNote[] = [
	{
		id: "1",
		author: "Sarah Johnson",
		authorInitials: "SJ",
		content:
			"Reviewed the flight change request. The original flight was cancelled by the airline, deviation is justified.",
		timestamp: "2024-01-15 10:30 AM",
	},
	{
		id: "2",
		author: "Mike Chen",
		authorInitials: "MC",
		content: "Contacted the traveler to confirm alternative flight details. Waiting for corporate card approval.",
		timestamp: "2024-01-15 2:45 PM",
	},
	{
		id: "3",
		author: "Sarah Johnson",
		authorInitials: "SJ",
		content: "Approved the deviation. Cost difference is within acceptable range.",
		timestamp: "2024-01-16 9:15 AM",
	},
];

export function AdminNotesCard({ isLoading = false }: { isLoading?: boolean }) {
	const [notes, setNotes] = useState<AdminNote[]>(mockNotes);
	const [isOpen, setIsOpen] = useState(false);
	const [newNote, setNewNote] = useState("");
	const [isEditOpen, setIsEditOpen] = useState(false);
	const [editingNote, setEditingNote] = useState<AdminNote | null>(null);
	const [editNoteContent, setEditNoteContent] = useState("");
	const [isDeleteOpen, setIsDeleteOpen] = useState(false);
	const [deletingNoteId, setDeletingNoteId] = useState<string | null>(null);

	const handleAddNote = () => {
		if (!newNote.trim()) return;

		const note: AdminNote = {
			id: Date.now().toString(),
			author: "Current Admin",
			authorInitials: "CA",
			content: newNote,
			timestamp: new Date().toLocaleString("en-US", {
				year: "numeric",
				month: "2-digit",
				day: "2-digit",
				hour: "2-digit",
				minute: "2-digit",
			}),
		};

		setNotes([...notes, note]);
		setNewNote("");
		setIsOpen(false);
	};

	const handleEditClick = (note: AdminNote) => {
		setEditingNote(note);
		setEditNoteContent(note.content);
		setIsEditOpen(true);
	};

	const handleSaveEdit = () => {
		if (!editingNote || !editNoteContent.trim()) return;

		setNotes(notes.map((note) => (note.id === editingNote.id ? { ...note, content: editNoteContent } : note)));
		setIsEditOpen(false);
		setEditingNote(null);
		setEditNoteContent("");
	};

	const handleDeleteClick = (noteId: string) => {
		setDeletingNoteId(noteId);
		setIsDeleteOpen(true);
	};

	const handleConfirmDelete = () => {
		if (!deletingNoteId) return;

		setNotes(notes.filter((note) => note.id !== deletingNoteId));
		setIsDeleteOpen(false);
		setDeletingNoteId(null);
	};

	if (isLoading) {
		return (
			<Card>
				<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
					<Skeleton className="h-6 w-32" />
					<Skeleton className="h-9 w-24" />
				</CardHeader>
				<CardContent>
					<div className="space-y-4">
						{[1, 2, 3].map((i) => (
							<div key={i} className="flex gap-3 p-3">
								<Skeleton className="h-8 w-8 rounded-full" />
								<div className="flex-1 space-y-2">
									<div className="flex items-center justify-between">
										<Skeleton className="h-4 w-24" />
										<Skeleton className="h-3 w-32" />
									</div>
									<Skeleton className="h-4 w-full" />
									<Skeleton className="h-4 w-3/4" />
								</div>
							</div>
						))}
					</div>
				</CardContent>
			</Card>
		);
	}

	return (
		<Card>
			<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
				<CardTitle>Admin Notes</CardTitle>
				<Dialog open={isOpen} onOpenChange={setIsOpen}>
					<DialogTrigger asChild>
						<Button size="sm">
							<Plus className="mr-2 h-4 w-4" />
							Add Note
						</Button>
					</DialogTrigger>
					<DialogContent>
						<DialogHeader>
							<DialogTitle>Add Admin Note</DialogTitle>
							<DialogDescription>
								Add an internal note about this travel deviation case. Notes are only visible to admins.
							</DialogDescription>
						</DialogHeader>
						<div className="py-4">
							<Textarea
								placeholder="Enter your note here..."
								value={newNote}
								onChange={(e) => setNewNote(e.target.value)}
								className="min-h-[120px]"
							/>
						</div>
						<DialogFooter>
							<Button variant="outline" onClick={() => setIsOpen(false)}>
								Cancel
							</Button>
							<Button onClick={handleAddNote}>Save Note</Button>
						</DialogFooter>
					</DialogContent>
				</Dialog>
			</CardHeader>
			<CardContent>
				<div className="space-y-4">
					{notes.length === 0 ? (
						<p className="text-sm text-muted-foreground text-center py-8">
							No admin notes yet. Add a note to get started.
						</p>
					) : (
						notes.map((note) => (
							<div key={note.id} className="flex gap-3 p-3 rounded-lg bg-muted/50">
								<Avatar className="h-8 w-8">
									<AvatarFallback className="text-xs">{note.authorInitials}</AvatarFallback>
								</Avatar>
								<div className="flex-1 space-y-1">
									<div className="flex items-center justify-between">
										<span className="text-sm font-medium">{note.author}</span>
										<span className="text-xs text-muted-foreground">{note.timestamp}</span>
									</div>
									<p className="text-sm text-foreground/90">{note.content}</p>
								</div>
								<div className="flex gap-1">
									<Button
										variant="ghost"
										size="icon"
										className="h-8 w-8"
										onClick={() => handleEditClick(note)}
									>
										<Pencil className="h-3.5 w-3.5" />
									</Button>
									<Button
										variant="ghost"
										size="icon"
										className="h-8 w-8 text-destructive hover:text-destructive"
										onClick={() => handleDeleteClick(note.id)}
									>
										<Trash2 className="h-3.5 w-3.5" />
									</Button>
								</div>
							</div>
						))
					)}
				</div>
			</CardContent>

			<Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
				<DialogContent>
					<DialogHeader>
						<DialogTitle>Edit Admin Note</DialogTitle>
						<DialogDescription>Make changes to your admin note below.</DialogDescription>
					</DialogHeader>
					<div className="py-4">
						<Textarea
							placeholder="Enter your note here..."
							value={editNoteContent}
							onChange={(e) => setEditNoteContent(e.target.value)}
							className="min-h-[120px]"
						/>
					</div>
					<DialogFooter>
						<Button
							variant="outline"
							onClick={() => {
								setIsEditOpen(false);
								setEditingNote(null);
								setEditNoteContent("");
							}}
						>
							Cancel
						</Button>
						<Button onClick={handleSaveEdit}>Save Changes</Button>
					</DialogFooter>
				</DialogContent>
			</Dialog>

			<AlertDialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
				<AlertDialogContent>
					<AlertDialogHeader>
						<AlertDialogTitle>Are you sure?</AlertDialogTitle>
						<AlertDialogDescription>
							This action cannot be undone. This will permanently delete the admin note.
						</AlertDialogDescription>
					</AlertDialogHeader>
					<AlertDialogFooter>
						<AlertDialogCancel
							onClick={() => {
								setIsDeleteOpen(false);
								setDeletingNoteId(null);
							}}
						>
							Cancel
						</AlertDialogCancel>
						<AlertDialogAction
							onClick={handleConfirmDelete}
							className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
						>
							Delete
						</AlertDialogAction>
					</AlertDialogFooter>
				</AlertDialogContent>
			</AlertDialog>
		</Card>
	);
}
```
