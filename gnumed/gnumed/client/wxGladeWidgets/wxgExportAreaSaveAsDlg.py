# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxgExportAreaSaveAsDlg(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgExportAreaSaveAsDlg.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((600, 250))
		self._LBL_header = wx.StaticText(self, wx.ID_ANY, _("\nDescribe the intended action.\n"))
		self._RBTN_save_as_files = wx.RadioButton(self, wx.ID_ANY, _("Files"))
		self._RBTN_save_as_archive = wx.RadioButton(self, wx.ID_ANY, _("&Archive"))
		self._CHBOX_encrypt = wx.CheckBox(self, wx.ID_ANY, _("en&crypted"), style=wx.CHK_2STATE)
		self._CHBOX_generate_metadata = wx.CheckBox(self, wx.ID_ANY, _("&metadata"), style=wx.CHK_2STATE)
		self._CHBOX_use_subdirectory = wx.CheckBox(self, wx.ID_ANY, _("use subdirectory"), style=wx.CHK_2STATE)
		self._LBL_directory = wx.StaticText(self, wx.ID_ANY, _("<shows default path computed at runtime>"), style=wx.ST_ELLIPSIZE_START)
		self._LBL_dir_is_empty = wx.StaticText(self, wx.ID_ANY, _("this path is/is not empty"))
		self._BTN_select_directory = wx.Button(self, wx.ID_ANY, _("Select"), style=wx.BU_EXACTFIT)
		self._BTN_open_directory = wx.Button(self, wx.ID_ANY, _("Open"), style=wx.BU_EXACTFIT)
		self._BTN_clear_directory = wx.Button(self, wx.ID_ANY, _("Clear"), style=wx.BU_EXACTFIT)
		self._BTN_save = wx.Button(self, wx.ID_SAVE, "")
		self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_RADIOBUTTON, self._on_save_as_files_selected, self._RBTN_save_as_files)
		self.Bind(wx.EVT_RADIOBUTTON, self._on_save_as_archive_selected, self._RBTN_save_as_archive)
		self.Bind(wx.EVT_CHECKBOX, self._on_save_as_encrypted_toggled, self._CHBOX_encrypt)
		self.Bind(wx.EVT_CHECKBOX, self._on_generate_metadata_toggled, self._CHBOX_generate_metadata)
		self.Bind(wx.EVT_CHECKBOX, self._on_use_subdirectory_toggled, self._CHBOX_use_subdirectory)
		self.Bind(wx.EVT_BUTTON, self._on_select_directory_button_pressed, self._BTN_select_directory)
		self.Bind(wx.EVT_BUTTON, self._on_open_directory_button_pressed, self._BTN_open_directory)
		self.Bind(wx.EVT_BUTTON, self._on_clear_directory_button_pressed, self._BTN_clear_directory)
		self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, self._BTN_save)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgExportAreaSaveAsDlg.__set_properties
		self.SetTitle(_("Saving export area items"))
		self.SetSize((600, 250))
		self._RBTN_save_as_files.SetToolTip(_("Save export items as individual files."))
		self._RBTN_save_as_files.SetValue(1)
		self._RBTN_save_as_archive.SetToolTip(_("Save export items as ZIP archive."))
		self._CHBOX_encrypt.SetToolTip(_("Use encryption ?\n\nWhen you save as files each file will be encrypted individually.\n\nWhen you save into an archive the ZIP archive itself will be encrypted rather than the files contained within. Encrypted archives will not include any patient data into the archive filename."))
		self._CHBOX_generate_metadata.SetToolTip(_("Generate metadata ?\n\nCheck if you want GNUmed to generate metadata describing the exported patient data and save it alongside the files.\n\nWhen saving into an archive metadata will always be included."))
		self._CHBOX_use_subdirectory.SetToolTip(_("Save into patient specific subdirectory ?\n\nIf checked GNUmed will use a suitable subdirectory within the selected path."))
		self._CHBOX_use_subdirectory.SetValue(1)
		self._LBL_directory.SetFont(wx.Font(9, wx.DEFAULT, wx.SLANT, wx.NORMAL, 0, ""))
		self._LBL_dir_is_empty.SetForegroundColour(wx.Colour(255, 127, 0))
		self._LBL_dir_is_empty.SetFont(wx.Font(9, wx.DEFAULT, wx.SLANT, wx.NORMAL, 0, ""))
		self._BTN_select_directory.SetToolTip(_("Select target directory for files or archive."))
		self._BTN_open_directory.SetToolTip(_("Open selected target directory in file browser."))
		self._BTN_clear_directory.SetToolTip(_("Clear selected target directory from any existing data."))
		self._BTN_clear_directory.Enable(False)
		self._BTN_save.SetToolTip(_("Save entries as files or archive."))
		self._BTN_cancel.SetToolTip(_("Abort saving entries."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgExportAreaSaveAsDlg.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
		__szr_dir_state = wx.BoxSizer(wx.HORIZONTAL)
		__szr_directory = wx.BoxSizer(wx.HORIZONTAL)
		__szr_save_as = wx.BoxSizer(wx.HORIZONTAL)
		__szr_main.Add(self._LBL_header, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__lbl_save_as = wx.StaticText(self, wx.ID_ANY, _("Save:"))
		__szr_save_as.Add(__lbl_save_as, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_save_as.Add(self._RBTN_save_as_files, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__szr_save_as.Add(self._RBTN_save_as_archive, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_save_as.Add(self._CHBOX_encrypt, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_save_as.Add(self._CHBOX_generate_metadata, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_save_as.Add(self._CHBOX_use_subdirectory, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
		__szr_main.Add(__szr_save_as, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__lbl_directory = wx.StaticText(self, wx.ID_ANY, _(u"\u21b3 Path:"))
		__szr_directory.Add(__lbl_directory, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
		__szr_directory.Add(self._LBL_directory, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_main.Add(__szr_directory, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__szr_dir_state.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_dir_state.Add(self._LBL_dir_is_empty, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__szr_dir_state.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_dir_state.Add(self._BTN_select_directory, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_dir_state.Add(self._BTN_open_directory, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_dir_state.Add(self._BTN_clear_directory, 0, wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_main.Add(__szr_dir_state, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__hline_bottom = wx.StaticLine(self, wx.ID_ANY)
		__szr_main.Add(__hline_bottom, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__szr_buttons.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_buttons.Add(self._BTN_save, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_buttons.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_buttons.Add(self._BTN_cancel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_buttons.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_main.Add(__szr_buttons, 0, wx.ALL | wx.EXPAND, 3)
		self.SetSizer(__szr_main)
		self.Layout()
		# end wxGlade

	def _on_save_as_files_selected(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_save_as_files_selected' not implemented!")
		event.Skip()

	def _on_save_as_archive_selected(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_save_as_archive_selected' not implemented!")
		event.Skip()

	def _on_save_as_encrypted_toggled(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_save_as_encrypted_toggled' not implemented!")
		event.Skip()

	def _on_generate_metadata_toggled(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_generate_metadata_toggled' not implemented!")
		event.Skip()

	def _on_use_subdirectory_toggled(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_use_subdirectory_toggled' not implemented!")
		event.Skip()

	def _on_select_directory_button_pressed(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_select_directory_button_pressed' not implemented!")
		event.Skip()

	def _on_open_directory_button_pressed(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_open_directory_button_pressed' not implemented!")
		event.Skip()

	def _on_clear_directory_button_pressed(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_clear_directory_button_pressed' not implemented!")
		event.Skip()

	def _on_save_button_pressed(self, event):  # wxGlade: wxgExportAreaSaveAsDlg.<event_handler>
		print("Event handler '_on_save_button_pressed' not implemented!")
		event.Skip()

# end of class wxgExportAreaSaveAsDlg
